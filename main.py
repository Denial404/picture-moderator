from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO
from better_profanity import profanity
import nltk
from nudenet import NudeDetector
# external functions

from server.ocr import detect_text_uri
import server.text_analysis as ta
import server.censoring as cen
import json as json

nltk.downloader.download('vader_lexicon')
nltk.downloader.download('stopwords')

app = Flask(__name__)
detector = NudeDetector()  # detector = NudeDetector('base') for the "base" version of detector.


@app.route('/')
def home():
    return "policing pictures for the people"

@app.route('/ocr', methods=["GET"])
def ocr():
    url = request.args.get("url", None)
    res = detect_text_uri(url)
    return jsonify(res)

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
    # gunicorn will not access this

    app.run(debug=True)
