from flask import Flask
from torahbot.lib.torahbot import TorahBot
import threading
import requests
import time

app = Flask(__name__)


@app.before_first_request
def run():
    def run_torahbot():
        torahbot = TorahBot()
        torahbot.run()
    thread = threading.Thread(target=run_torahbot)
    thread.start()


@app.route("/")
def hello():
    return "Hello Torah!"


if __name__ == "__main__":
    app.run()
