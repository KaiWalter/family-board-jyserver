#!/usr/env/bin python3

import argparse
import logging
import time

from jyserver.Server import Client, Server


class App(Client):
    def __init__(self):
        pass

    def main(self):
        while True:
            self.js.dom.message.innerHTML = "calendar refresh"
            time.sleep(1)
            self.js.dom.message.innerHTML = "..."
            time.sleep(15)


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--logfile', required=False,
                        dest='logfile', help='Name of log file.', type=str, default='server.log')
    parser.add_argument('-a', '--ip', required=False,
                        dest='address', help='IP address to host on.', type=str, default=None)
    parser.add_argument('-p', '--port', required=False,
                        dest='port', help='Port to host on.', type=int, default=80)
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    # configure
    args = parse_args()

    logging.basicConfig(
        filename=args.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    # main process
    httpd = Server(App, ip=args.address, port=args.port, verbose=False)
    logging.info('serving at port %s', httpd.port)
    print('ready')
    httpd.start()
