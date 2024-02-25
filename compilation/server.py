from flask import Flask, jsonify, request, abort
import subprocess
import sys
import json
import hashlib
import os

# curl -X POST -H "Content-Type: application/json" -d '{"name": "John", "age": 30}' http://localhost:5000/
# example req
# curl -X POST -d "data=HelloWorld" http://localhost:5000/

app = Flask(__name__)

# A simple GET endpoint
@app.route('/', methods=['GET'])
def get_data():
    data = {'message': 'This is a GET request'}
    return jsonify(data)

# A simple POST endpoint
@app.route('/', methods=['POST'])
def post_data():

    data = request.get_data()
    data_str = data.decode('utf-8')
    print(data_str)

    extension = ".c"

    # hash contents
    sha256_hash = hashlib.sha256(data_str.encode()).hexdigest()

    # save string as c file
    file_name = sha256_hash + extension
    print(file_name)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data_str)

    # copy file to container
    # docker cp input_file.c container_id:/path/in/container

    # compile code
    # docker exec -it container_id /path/in/container/compile.sh input_file.c

    compiler = 'gcc'
    subprocess.run(['sh','compile.sh', compiler, file_name])
    

    if data is not None:
        return jsonify({'message': f'Received file: {data_str}'})
    else:
        return jsonify({'error': 'No file provided'}), 400

    # basically, gcc file and send to S3
    

if __name__ == '__main__':
    # app.run(debug=True)
    # set IPV4 as an environment variable..
    # export IPV4="YOUR_IP_ADDR"
    ip_addr = os.getenv("IPV4")
    app.run(host=ip_addr, port=9000)
