# AUTHORS: Robin Lee - execute.py

# PURPOSE:
#      Take in arbritary code and execute it.
#      Placeholder code, until AWS lambda function is done.

##############################################################################

import subprocess
def execute_c_program(file):

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
            out +="program executed successfully."
        else:
            out +="program terminated with an error."

    except FileNotFoundError:
        out +="Error: The specified program does not exist."

    return out