# Execution VMs

With our system architecture, we have a VM that listens for incoming requests to be executed.

At the server (execute_server.py), these requests would be taken in and parsed into 3 components: Code, Compiler, Compiler_Version

In order to retrieve the correct compiled code from the S3, the Code, Compiler, and Compiler_Version are appended together and hashed using SHA256.

With this hash, we can easily retrieve from the S3 bucket and execute the code with AWS lambda function.


