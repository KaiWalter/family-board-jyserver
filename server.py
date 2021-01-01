#!/usr/env/bin python3

import argparse
import logging
import time

import jyserver.Flask as jsf
from flask import Flask, render_template, request

app = Flask(__name__)


@jsf.use(app)
class App:
    def __init__(self):
        pass

    @jsf.task
    def main(self):
        while True:
            self.js.dom.message.innerHTML = "calendar refresh"
            time.sleep(1)
            self.js.dom.message.innerHTML = "..."
            time.sleep(15)


@app.route('/')
def index_page(name=None):
    App.main()
    return App.render(render_template('index.html'))


@app.route('/msatoken')
def msa_token():
    return App.render(render_template('msatoken.html'))


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--logfile', required=False,
                        dest='logfile', help='Name of log file.', type=str, default='server.log')
    parser.add_argument('-a', '--ip', required=False,
                        dest='address', help='IP address to host on.', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', required=False,
                        dest='port', help='Port to host on.', type=int, default=8080)
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    # configure
    args = parse_args()

    logging.basicConfig(
        filename=args.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    # main process
    logging.info('serving at on address %s port %s', args.address, args.port)
    app.run(host=args.address, port=args.port)
