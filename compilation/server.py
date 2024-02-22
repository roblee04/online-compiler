from flask import Flask, jsonify, request, abort
import json

# curl -X POST -H "Content-Type: application/json" -d '{"name": "John", "age": 30}' http://localhost:5000/
# example req

app = Flask(__name__)

# A simple GET endpoint
@app.route('/get', methods=['GET'])
def get_data():
    data = {'message': 'This is a GET request'}
    return jsonify(data)

# A simple POST endpoint
@app.route('/post', methods=['POST'])
def post_data():
    if not request.is_json:
        abort(400)

    data = request.get_json()
    response = {'message': 'This is a POST request:', 'data': data}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)