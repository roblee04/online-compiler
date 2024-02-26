FROM your_base_image

# Install the AWS CLI
RUN apt-get update && apt-get install -y awscli

# init docker cp compile.sh container_id:/path/in/container