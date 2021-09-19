from flask import Flask, request, jsonify
from better_profanity import profanity
# external functions
from server.ocr import detect_text_uri
import server.text_analysis as ta
import nltk

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

def server_start():
    nltk.downloader.download('vader_lexicon')
    nltk.downloader.download('stopwords')
    app.run(debug=True)

if __name__ == "__main__":
    server_start()
