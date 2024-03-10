# AUTHORS: Robin Lee, Nolan Anderson - compile_server.py

# PURPOSE:
#      To be run on a VM to issue compilations for various c/c++ compilers.
#      Route code compilation requests to containers with a specific compiler.

# SUPPORTED APIs:
#   1. testing uptime of server via GET
#   2. Compile code. Recieve code and compiler to be used. Route to correct container.

##############################################################################

# USAGE:
#   curl --data-binary "CODE_AS_STRING" http://YOUR_IP:9000/COMPILER/VERSION

# Example Query
#   curl --data-binary "@test.c" http://localhost:9000/gcc/13.2.1

# Example Output:
#   {"message":"Received file: #include <stdio.h>\nint main() {\n   // printf() displays the string inside quotation\n   printf(\"Hello, World!\");\n   return 0;\n}"}

##############################################################################

from flask import Flask, jsonify, request, abort
import subprocess
import sys
import json
import hashlib
import os
import s3_upload
import docker

##############################################################################
# App Creation
app = Flask(__name__)

##############################################################################
# A Testing Endpoint
@app.route('/', methods=['GET'])
def get_data():
    data = {'message': 'This is a GET request'}
    return jsonify(data)

##############################################################################
# Receive code to be compiled. args: code, compiler, compiler version
@app.route('/<compiler>/<version>', methods=['POST'])
def post_data(compiler: str, version:str):
    # Take in Code and decode
    data = request.get_data()
    data_str = data.decode('utf-8')

    # check to see if we have any data, bad request if nothing is provided
    if (len(data_str) == 0):
        return jsonify("No source code provided."), 400

    # find extension from compiler
    cpp_compilers = ["clang++", "g++", "icpx"]
    if (compiler in cpp_compilers):
        extension = ".cpp"
    else:
        extension = ".c"

    # hash contents
    header = compiler + version
    sha256_hash = hashlib.sha256((data_str + header).encode()).hexdigest()

    # save string as c/cpp file
    file_name = sha256_hash + extension
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data_str)

    # get docker client
    client = docker.from_env()

    # script path (docker needs absolute references for volume)
    script_path = sys.path[0]

    volumes = []
    # mount for getting source file in container
    volumes.append(script_path + "/" + file_name + ":/file" + extension)
    # mount compilation folder on host as out folder in container
    volumes.append(script_path + ":/out")

    # image names are formatted name:tag
    compiler_to_image_name = {"gcc": "gcc", "g++": "gcc", "clang": "clang", \
        "clang++": "clang", "tcc": "tcc", "icx": "oneapi", "icpx": "oneapi"}
    image_name = compiler_to_image_name[compiler] + ":" + version
    # need to use full path for intel compilers
    if (compiler == "icx" or compiler == "icpx"):
        compiler = "/opt/intel/oneapi/compiler/latest/bin/" + compiler

    # get command to run
    cmd = compiler + " file" + extension + " -o /out/" + sha256_hash
    
    try:
        # run the command on the appropriate container
        client.containers.run(image_name, cmd, volumes=volumes)
    except docker.errors.ContainerError as e:
        # compilation failed (skill issue)
        # get stderr for compilation error message
        stderr_result = e.stderr.decode("utf-8")
        # delete source file
        os.remove(file_name)
        return jsonify(stderr_result), 500
    except docker.errors.ImageNotFound as e:
        # missing image
        os.remove(file_name)
        return jsonify("Docker: Image for the selected compiler and version is missing."), 500
    except Exception as e:
        # some other error
        os.remove(file_name)
        return jsonify("Docker: " + str(e) + "."), 500

    # after compilation delete the source from local storage
    os.remove(file_name)

    # upload the compiled executable to s3 bucket
    try:
        s3_upload.upload(sha256_hash)
    except Exception as e:
        # some error
        # delete executable file
        os.remove(sha256_hash)
        return jsonify("S3: " + str(e) + "."), 500

    # after upload remove executable from local storage
    os.remove(sha256_hash)

    return jsonify({'message': f'Received file: {data_str}'}), 200


##############################################################################
# Start the server
if __name__ == '__main__':
    # app.run(debug=True)
    # set IPV4 as an environment variable..
    # export IPV4="YOUR_IP_ADDR"
    # ip_addr = os.getenv("IPV4")

    # set script directory as current directory
    os.chdir(sys.path[0])

    # start app
    app.run(host="0.0.0.0", port=9000)
