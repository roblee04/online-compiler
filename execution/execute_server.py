# AUTHORS: Robin Lee - execute_server.py

# PURPOSE:
#      To be run on a VM to issue executions of arbritrary code.
#      AWS Lamdba functions are used for sandboxing.

# SUPPORTED APIs:
#   1. testing uptime of server via GET
#   2. Execute code. 

##############################################################################

# USAGE:
#   curl --data-binary "CODE_AS_STRING" http://YOUR_IP:9870/COMPILER/VERSION

# Example Query
#   curl --data-binary "@test.c" http://localhost:9870/gcc/13.2.1

# Example Output:
#   {"message":"Output: Hello, World! Return code: 0 C program executed successfully."}


##############################################################################

from flask import Flask, jsonify, request, abort
import sys
import json
import hashlib
import os
import requests
import lambda_function
import boto3

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
# Receive code to executed. args: code, compiler, compiler version
@app.route('/<compiler>/<version>', methods=['POST'])
def post_data(compiler: str, version:str):
    # Take in Code and decode
    data = request.get_data()
    data_str = data.decode('utf-8')

    # recalculate hash contents
    header = compiler + version
    sha256_hash = hashlib.sha256((data_str + header).encode()).hexdigest()

    # get file from S3

    file_name = sha256_hash
    
    # send to aws lambda function to execute

    # Create a Lambda client
    lambda_client = boto3.client('lambda', region_name='us-west-1')  # Specify your region

    # Define the Lambda function name or ARN
    function_name = 'execute_code'

    # Define the payload you want to send to your Lambda function
    payload = {
    "filename": file_name
    }

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # Use 'Event' for asynchronous execution
        Payload=json.dumps(payload),
    )

    res = response['Payload'].read().decode("utf-8")
    out = json.loads(res)

    # out = lambda_function.lambda_handler(event, None)


    if data is not None:
        return jsonify({'message': f'{out["body"]}'}), 200
    else:
        return jsonify({'error': 'No file provided'}), 400

    
##############################################################################
# Start the server

if __name__ == '__main__':
    # app.run(debug=True)
    # set IPV4 as an environment variable..
    # export IPV4="YOUR_IP_ADDR"
    # ip_addr = os.getenv("IPV4")
    app.run(host="0.0.0.0", port=9870)
