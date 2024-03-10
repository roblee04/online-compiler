import subprocess
import os
import boto3
import json

s3 = boto3.client('s3')

def download_file_from_s3(bucket_name, file_key, local_file_path):
    s3.download_file(bucket_name, file_key, local_file_path)

def execute_program(file):

    out = ""
    try:
        # execute compiled program
        process = subprocess.Popen(file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Check if there was any output to stdout
        if stdout:
            out += "Output: "
            out +=stdout.decode('utf-8') + "\n\n"

        # Check if there was any output to stderr
        if stderr:
            out +="Error: "
            out +=stderr.decode('utf-8') + "\n\n"

        # Get the return code of the process
        return_code = process.returncode
        out += f"Return code: {return_code}\n\n" 

        # Check if the process terminated successfully
        if return_code == 0:
            out +="program executed successfully."
        else:
            out +="program terminated with an error."

    except FileNotFoundError:
        out +="Error: The specified program does not exist."

    return out

def lambda_handler(event, context):
    # print(json.dumps(event))
    # Specify the S3 bucket name and file key
    bucket_name = 'codecompiler241'
    file_key = event["filename"]
    # Download the executable from S3 to /tmp
    local_file_path = '/tmp/' + file_key
    download_file_from_s3(bucket_name, file_key, local_file_path)
    
    # Set the executable file's permissions to allow execution
    os.chmod(local_file_path, 0o755)
    
    # Run the downloaded executable
    result = execute_program(local_file_path)
    
    # Return the output of the executable
    return {
        "statusCode": 200,
        "body": result
    }
