from flask import Flask
from threading import Thread
import sys

app = Flask('')

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def home():
    return "fessor is live. poggers."

def run():
  cli = sys.modules['flask.cli']
  cli.show_server_banner = lambda *x: None
  print('starting flask...')
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
