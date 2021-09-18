# Import module
from nudenet import NudeDetector
from nudenet import NudeClassifier
from flask import Flask, request, jsonify

import text_analysis as ta

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "what's good"

@app.route("/nude-net", methods=["GET"])
def nude_net():
    image = "./jackblack.png"
    detector = NudeDetector() # detector = NudeDetector('base') for the "base" version of detector.
    detector = detector.detect(image)
    classifier = NudeClassifier()
    pokemon = classifier.classify(image)

    return jsonify({"detector": detector, "classifier": pokemon})


@app.route("/analyze-text", methods=["GET"])
def analyze_text():
    text = request.args.get('text')
    analysis = {
        'text': text,
        'scores': ta.sentiment(text)
    }
    return jsonify({'analysis': analysis})


if __name__ == "__main__":
    # initialize detector (downloads the checkpoint file automatically the first time)
    app.run(port=8080, debug=True)
