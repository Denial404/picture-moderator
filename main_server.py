from flask import Flask, request, jsonify
from threading import Thread
from main_bot import client
# external functions
from server.ocr import detect_text_uri
from server.censoring import censorImage

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
    url = request.args.get("nsfw-url", None)
    return url

def server_start():
    # t = Thread(target=run)
    # t.start()
    app.run(debug=True)


if __name__ == "__main__":
    server_start()