from flask import Flask, request, jsonify

# external functions
from server.ocr import detect_text_uri
app = Flask(__name__)

@app.route("/")
def home():
    return "hello!"


@app.route('/ocr', methods=["GET"])
def ocr():
    url = request.args.get("url", None)
    return jsonify(detect_text_uri(url))

if __name__ == "__main__":
    app.run(debug=True)
