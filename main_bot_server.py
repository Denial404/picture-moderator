from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "我很喜欢冰激淋"

def run():
  app.run(host='0.0.0.0',port=8080)

def server():
    t = Thread(target=run)
    t.start()