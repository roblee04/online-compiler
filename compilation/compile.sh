#usage ./compile.sh gcc your_file.c

#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <compiler> <file>"
    exit 1
fi

compiler=$1
file_name=$2

# Compile the file using the selected compiler
$compiler $file_name -o ${file_name%.*}

# also store into S3
cp ${file_name%.*} ../execution