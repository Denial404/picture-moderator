from flask import Flask, request, jsonify
from threading import Thread
from main_bot import client
from better_profanity import profanity
# external functions
from server.ocr import detect_text_uri
import server.text_analysis as ta
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "policing pictures for the people"

@app.route('/ocr', methods=["GET"])
def ocr():
    url = request.args.get("url", None)
    res = detect_text_uri(url)
    return jsonify(res)

@app.route('/pic-analysis', methods=["GET"])
def pic_analysis():
    url = request.args.get("url", None)
    return url


@app.route("/analyze-text", methods=["GET"])
def analyze_text():
    text = request.args.get('text')
    bad = profanity.contains_profanity(text)
    analysis = {
        'text': text,
        'scores': ta.sentiment(text),
        'profanity': bad
    }
    return jsonify({'analysis': analysis})

if __name__ == "__main__":
    app.run(debug=True)