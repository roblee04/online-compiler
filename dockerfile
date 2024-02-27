# Use the official Ubuntu 20.04 image
FROM ubuntu:20.04

# Install GCC, Clang, G++, and other necessary build tools
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    clang \
    llvm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install specific versions of compilers (e.g., GCC 9, Clang 10)
RUN apt-get update && apt-get install -y \
    gcc-9 \
    g++-9 \
    clang-10 \
    llvm-10 \
    && rm -rf /var/lib/apt/lists/*

# Install additional compilers (if needed)
# RUN apt-get update && apt-get install -y \
#    gcc-8 \
#    g++-8 \
#    clang-9 \
#    llvm-9 \
#    && rm -rf /var/lib/apt/lists/*

# Install the AWS CLI using the official AWS installation script
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip \
    && apt-get remove -y --purge \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Print AWS CLI version to verify installation
RUN aws --version

# Set the working directory to /app
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Set the default command to bash
CMD ["bash"]
