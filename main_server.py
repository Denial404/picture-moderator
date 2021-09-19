from flask import Flask, request, jsonify
from better_profanity import profanity
import nltk
from nudenet import NudeDetector
# external functions
from server.ocr import detect_text_uri
import server.text_analysis as ta
import server.censoring as cen

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

@app.route('/pic-analysis', methods=["GET"])
def pic_analysis():
    print("PIC-ANALSIS, BEGINNING")
    nsfw_path = request.args.get("nsfw_path", None)
    sfw_path = request.args.get("sfw_path", None)
    detectorJson = detector.detect(nsfw_path)
    result_path = cen.censorImage(detectorJson, nsfw_path, sfw_path)
    print("PIC-ANALYSIS", jsonify({"path": result_path}))
    return jsonify({"path": result_path})


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
