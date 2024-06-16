from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 * num2
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
