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
EXECUTE_IP = os.getenv("EXECIP")

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
    data = request.get_data()
    code = data.get('code')
    

    #   curl --data-binary "@test.c" http://localhost:9870/gcc/13.2.1
    # Perform compilation logic here

    return jsonify({'success': True, 'code': code}), 400


##############################################################################
# Send current code as request, see execution result
@app.route('/api/run', methods=['POST'])
def run():
    # Load the compiled binary and execute it
    # Capture the output and return it as a JSON response
    print("run")

    output = "Your output here"
    return jsonify({'output': output}), 400


##############################################################################
# Start the server

if __name__ == '__main__':
    
    app.run(debug=True)