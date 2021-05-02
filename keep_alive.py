from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "This, discord bot created by the 53 BUS GANG IS RUNNING"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()