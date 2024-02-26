from flask import Flask, jsonify, request, abort
import sys
import json
import hashlib
import os
import execute

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

    # recalculate hash contents
    sha256_hash = hashlib.sha256(data_str.encode()).hexdigest()

    # get file from S3

    # save string as file
    file_name = sha256_hash
    
    # send to aws lambda function to execute
    
    out = execute.execute_c_program(file_name)

    # remove file from local storage
    os.remove(file_name)

    if data is not None:
        return jsonify({'message': f'{out}'})
    else:
        return jsonify({'error': 'No file provided'}), 400

    # basically, gcc file and send to S3
    

if __name__ == '__main__':
    # app.run(debug=True)
    # set IPV4 as an environment variable..
    # export IPV4="YOUR_IP_ADDR"
    ip_addr = os.getenv("IPV4")
    app.run(host=ip_addr, port=9870)