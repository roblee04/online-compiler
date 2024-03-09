# AUTHORS: Robin Lee - s3_upload.py

# PURPOSE:
#      To upload the file to an S3 bucket

# USAGE:
#       python s3_upload.py FILENAME

##############################################################################
import os
import boto3
import sys
import json
from flask import jsonify
import logging
from botocore.exceptions import ClientError


##############################################################################
# helper to upload to s3
def upload_to_s3(s3, file_name, bucket):
    
    object_name = os.path.basename(file_name)

    try:
        s3.upload_file(file_name, bucket, object_name)

    except ClientError as e:
        logging.error(e)
        return jsonify({'error': f'{e}'}), 400
    return jsonify({'success': True}), 200


##############################################################################
# init variables
def main():
    s3 = boto3.client('s3')
    file_name = sys.argv[1]
    bucket = 's3-ide-demo'
    upload_to_s3(s3, file_name, bucket)

    
##############################################################################
# call main
if __name__ == '__main__':
    main()