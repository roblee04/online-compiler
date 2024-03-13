# online-compiler
Simple online code sandbox, hosted on AWS EC2 instances. 

Currently supports:
### C
- GCC 5.4.0
- GCC 7.5.0
- GCC 9.4.0
- Clang 3.8.0
- Clang 6.0.0
- Clang 10.0.0
- TCC Latest

### C++
- G++ 5.4.0
- G++ 7.5.0
- G++ 9.4.0
- Clang++ 3.8.0
- Clang++ 6.0.0
- Clang++ 10.0.0



Execution is sandboxed via AWS lambda functions.

Containers are spun up on every call for compilation. Docker-compose is used to build the images (each image has specific compiler versions).

Architecture diagram is shown.

![alt text](./cloud%20computing%20arch%202.drawio.png)

# To set up EC2 instances:
Make sure that EC2s have some exposed ports and can be accessed by all TCP (0.0.0.0). All http / https / connections is a bait permissions group.

Assuming EC2's with Amazon Linux...

## Web Server:
```bash
sudo yum install python-pip 
git clone https://github.com/roblee04/online-compiler


cd online-compiler 
pip install -r requirements.txt

cd webapp 
export COMPIP="http://COMPILEIP:PORT" 
export EXECIP="http://EXECUTEIP:PORT"

python3 webapp.py
```

## Compilation VM:

```bash
sudo yum install python-pip 
git clone https://github.com/roblee04/online-compiler

# install Docker and Docker-Compose
sudo yum update -y 
sudo amazon-linux-extras install docker 
sudo yum install docker 
sudo service docker start  
sudo usermod -a -G docker ec2-user 
docker info

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose 

sudo chmod +x /usr/local/bin/docker-compose 
docker-compose version

# setup aws iam for S3, user and pass
aws configure

cd online-compiler \
pip install -r requirements.txt \

cd compilation \
docker-compose build \
python3 compile_server.py
```

## Execution VM:


```bash 
sudo yum install python-pip 

git clone https://github.com/roblee04/online-compiler

# setup aws iam for S3 
aws configure

cd online-compiler 
pip install -r requirements.txt

cd execution 
python3 execute_server.py
```

## Setup AWS Lambda function
Assuming AWS console setup.

copy paste the code in execution/lambda_function.py for the logic.

Allow access to S3 Buckets, allow to be invoked anywhere.

test with a sample payload: {"filename":"test"}

## Setup the S3 Bucket
Name your S3 bucket something. Probably good to set some perms as well.

Change the bucket name in execution/lambda_function.py to be your bucket name. (default is called 'codecompiler241').

Change the bucket name in compilation/s3_upload.py to be your bucket name. (default is called 'codecompiler241')