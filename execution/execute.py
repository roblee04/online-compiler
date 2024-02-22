import subprocess
import sys

def execute_c_program():

    # download file from S3 Bucket
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/download-objects.html
    file = sys.argv[1]

    try:
        # execute compiled program
        process = subprocess.Popen('./' + file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Check if there was any output to stdout
        if stdout:
            print("Output:")
            print(stdout.decode('utf-8'))

        # Check if there was any output to stderr
        if stderr:
            print("Error:")
            print(stderr.decode('utf-8'))

        # Get the return code of the process
        return_code = process.returncode
        print("Return code:", return_code)

        # Check if the process terminated successfully
        if return_code == 0:
            print("C program executed successfully.")
        else:
            print("C program terminated with an error.")

    except FileNotFoundError:
        print("Error: The specified C program does not exist.")

execute_c_program()
