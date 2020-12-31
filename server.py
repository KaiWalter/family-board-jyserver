#!/usr/env/bin python3

from jyserver.Server import Server, Client
import time

class App(Client):
    def __init__(self):
        pass

    def main(self):
        while True:
            self.js.dom.message.innerHTML = "calendar refresh"
            time.sleep(1)
            self.js.dom.message.innerHTML = "..."
            time.sleep(15)

if __name__ == "__main__":

    httpd = Server(App, ip='0.0.0.0', verbose=False)
    print("serving at port", httpd.port)
    httpd.start()