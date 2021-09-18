# Import module
from nudenet import NudeDetector
from nudenet import NudeClassifier
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home(): 
  return "what's good"
  
@app.route("/nude-net", methods=["GET"])
def nudeNet(): 
  image = "./jackblack.png"
  detector = NudeDetector() # detector = NudeDetector('base') for the "base" version of detector.
  detector = detector.detect(image)
  classifier = NudeClassifier()
  pokemon = classifier.classify(image)


  return jsonify({"detector": detector, "classifier": pokemon})


if __name__ == "__main__":
  # initialize detector (downloads the checkpoint file automatically the first time)
  app.run(port=8080, debug=True)
