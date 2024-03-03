from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def sandbox():
    return render_template('index.html')


@app.route('/api/compile', methods=['POST'])
def compile():
    data = request.get_json()
    code = data.get('code')
    print("compile")

    # Perform compilation logic here
    # For example, you can use the subprocess module to call a C++ compiler
    # Save the compiled binary for later execution

    return jsonify({'success': True})

@app.route('/api/run', methods=['POST'])
def run():
    # Load the compiled binary and execute it
    # Capture the output and return it as a JSON response
    print("run")

    output = "Your output here"
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)