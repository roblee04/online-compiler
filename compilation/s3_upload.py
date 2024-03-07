import os
import boto3
import json
import logging
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def upload_file(file_name, bucket, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def lambda_handler(event, context):
    print(json.dumps(event))
    # Specify the S3 bucket name and file name
    bucket_name = 'online-compiler'
    file_name = event["filename"]
    print("file_name", file_name)
    
    result = upload_file(file_name, bucket_name)
    
    # Return the output of the executable
    return {
        "statusCode": 200,
        "body": result
    }
