import subprocess
def execute_c_program(file):

    # download file from S3 Bucket
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/download-objects.html
    # file = sys.argv[1]
    out = ""
    try:
        # execute compiled program
        process = subprocess.Popen('./' + file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Check if there was any output to stdout
        if stdout:
            out += "Output: "
            out +=stdout.decode('utf-8') + " "

        # Check if there was any output to stderr
        if stderr:
            out +="Error: "
            out +=stderr.decode('utf-8') + " "

        # Get the return code of the process
        return_code = process.returncode
        out += f"Return code: {return_code} " 

        # Check if the process terminated successfully
        if return_code == 0:
            out +="C program executed successfully."
        else:
            out +="C program terminated with an error."

    except FileNotFoundError:
        out +="Error: The specified C program does not exist."

    return out