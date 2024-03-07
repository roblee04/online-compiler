# AUTHORS: Robin Lee - compile_server.py

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

    # find extension from compiler
    cmp_to_ext = {"gcc": ".c", "clang": ".c", "clang++": ".cpp", "g++": ".cpp"}

    extension = cmp_to_ext[compiler]

    # hash contents
    header = compiler + version
    sha256_hash = hashlib.sha256((data_str + header).encode()).hexdigest()

    # save string as c file
    file_name = sha256_hash + extension
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data_str)

    # Find correct container

    # copy file to container
    # docker cp input_file.c container_id:/path/in/container

    # compile code to container
    # docker exec -it container_id /path/in/container/compile.sh input_file.c

    result = subprocess.run(['sh','compile.sh', compiler, file_name], capture_output=True)
    stderr_result = result.stderr.decode('utf-8')  # Standard error as a string

    # after compilation delete the file from local storage
    # os.remove(file_name)

    if result.returncode == 0:
        #uploading the compiled exe to s3 bucket
        directory_path = "../execution/"
        file_path = os.path.join(directory_path, sha256_hash)
        event = {
            "filename": file_path
        }
        uploaded_to_S3 = s3_upload.lambda_handler(event, None)
        print(uploaded_to_S3)
        return jsonify({'message': f'Received file: {data_str}'}), 200
    else:
        substring = "undefined"
        start_index = stderr_result.find("error")
        end_index = stderr_result.find("generated")
        if start_index != -1 and end_index != -1:
            substring = stderr_result[start_index:end_index + len("generated")]
        return jsonify(substring), 400


##############################################################################
# Start the server
if __name__ == '__main__':
    # app.run(debug=True)
    # set IPV4 as an environment variable..
    # export IPV4="YOUR_IP_ADDR"
    # ip_addr = os.getenv("IPV4")
    app.run(host="0.0.0.0", port=9000)
