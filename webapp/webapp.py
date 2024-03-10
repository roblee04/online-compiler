# AUTHORS: Robin Lee - webapp.py

# PURPOSE:
#      To host the webpage and make corresponding requests to compile and execute code.

# SUPPORTED APIs:
#   1. Display Webpage
#   2. Send request to compile and display result.
#   3. Send request to execute and display result.

##############################################################################

# USAGE:
#   visit localhost:5000


##############################################################################
from flask import Flask, render_template, jsonify, request
import os
import requests

##############################################################################
# Environment Variable Declarations
# export IP="YOUR_IP_ADDR"
COMPILE_IP = os.getenv("COMPIP")
# COMPILE_IP = "http://127.0.0.1:9000"
EXECUTE_IP = os.getenv("EXECIP")
# EXECUTE_IP = "http://127.0.0.1:9870"

##############################################################################
# App Creation
app = Flask(__name__, template_folder='../templates', static_folder='../static')

##############################################################################
# Render default webpage
@app.route('/')
def sandbox():
    return render_template('index.html')


##############################################################################
# Send current code as a request to be compiled
@app.route('/api/compile', methods=['POST'])
def compile():
    data = request.get_json()
    code = data.get('code')
    
    #   curl --data-binary "@test.c" http://localhost:9870/gcc/13.2.1
    # Perform compilation logic here
    compiler, version = data.get('compiler').split()
    url = f"{COMPILE_IP}/{compiler}/{version}"

    # try else exception
    try:
        response = requests.post(url, code)
        if response.status_code == 200:
            return jsonify({'success': True, 'code': data}), 200
        else:
            #raise Exception("Compile Server Error")
            raise Exception(response.text)
    
    except Exception as err_msg:
        return str(err_msg), 400


##############################################################################
# Send current code as request, see execution result
@app.route('/api/run', methods=['POST'])
def run():
    data = request.get_json()
    code = data.get('code')

    # Load the compiled binary and execute it
    # Capture the output and return it as a JSON response
    compiler, version = data.get('compiler').split()
    url = f"{EXECUTE_IP}/{compiler}/{version}"

    # try else exception
    try:
        response = requests.post(url, code)
        print(response.json())

        if response.status_code == 200:
            output = response.json()['message']
            return jsonify({'output': output}), 200
        else:
            raise Exception("Execute Server Error")
    
    except Exception as err_msg:
        return jsonify({'error': err_msg.args[0]}), 400


##############################################################################
# Start the server

if __name__ == '__main__':
    
    app.run(debug=True, host="0.0.0.0", port=5000)
