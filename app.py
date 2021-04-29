from flask import (
    Flask, request, jsonify
)
app = Flask(__name__)

@app.route("/")
def main():
    return "Don't visit here!"

@app.route("/compare", methods = ['POST'])
def recieve_request():
    print(request.files['source'])
    response = jsonify(score=100)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
