from flask import Flask, jsonify, request, abort
import subprocess
import sys
import json

# curl -X POST -H "Content-Type: application/json" -d '{"name": "John", "age": 30}' http://localhost:5000/
# example req
# curl -X POST -d "data=HelloWorld" http://localhost:5000/

app = Flask(__name__)

# A simple GET endpoint
@app.route('/', methods=['GET'])
def get_data():
    data = {'message': 'This is a GET request'}
    return jsonify(data)

# A simple POST endpoint
@app.route('/', methods=['POST'])
def post_data():

    data = request.get_data()
    data_str = data.decode('utf-8')
    print(data_str)

    # save string as file
    file_name = "test.c"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data_str)

    # copy file to container
    # docker cp input_file.c container_id:/path/in/container

    # compile code
    # docker exec -it container_id /path/in/container/compile.sh input_file.c
    compiler = 'gcc'
    subprocess.run(['sh','compile.sh', compiler, file_name])


    if data is not None:
        return jsonify({'message': f'Received file: {data_str}'})
    else:
        return jsonify({'error': 'No file provided'}), 400

    # basically, gcc file and send to S3
    

if __name__ == '__main__':
    app.run(debug=True)


def compile_program():

    file = sys.argv[1]
    with open(file) as f: string = f.read()

    try:
        # Replace 'your_program.c' with the name of your C source file
        # Replace 'your_program' with the desired name of the executable
        subprocess.run(['clang', file, '-o', file], check=True)
        print("C program compiled successfully.")
    except subprocess.CalledProcessError as e:
        print("Error: Compilation failed with return code:", e.returncode)