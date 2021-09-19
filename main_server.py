from flask import Flask, request, jsonify
from threading import Thread
from main_bot import client
# external functions
from server.ocr import detect_text_uri
import server.text_analysis as ta

import os

app = Flask(__name__)

@app.route('/')
def home():
    return "policing pictures for the people"

@app.route('/ocr', methods=["GET"])
def ocr():
    url = request.args.get("url", None)
    return jsonify(detect_text_uri(url))

@app.route('/pic-analysis', methods=["GET"])
def pic_analysis():
    url = request.args.get("url", None)
    return url


@app.route("/analyze-text", methods=["GET"])
def analyze_text():
    text = request.args.get('text')
    analysis = {
        'text': text,
        'scores': ta.sentiment(text)
    }
    return jsonify({'analysis': analysis})


if __name__ == "__main__":
    app.run(debug=True)