# Compilation VM

With our system architecture, we have a VM that listens for incoming requests and containers within that VM that each hold specific compilers (e.g. GCC 9.4.0, Clang 10.0.0, etc.). Furthermore, after compilation, the compiled code is sent to an S3 bucket.

At the server (compiler_server.py), these requests would be taken in and parsed into 3 components: Code, Compiler, Compiler_Version

Firstly, the Code, Compiler, and Compiler_Version are appended together and hashed using SHA256 for easy retrieval from S3.

Secondly, the code is routed to the corresponding container that has the Compiler + Compiler Version.In this container, the code is compiled. Then, the output is copied to S3.

The container images used by the compilation VM were created using the provided *docker-compose.yml* and the following command:

`docker compose build`
