#!/usr/env/bin python3

from jyserver.Server import Server, Client
import time

class App(Client):
    def __init__(self):
        self.running = True

    def reset(self):
        self.start0 = time.time()
        self.js.dom.time.innerHTML = "{:.1f}".format(0)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        self.js.dom.b2.innerHTML = "Restart"
        self.js.dom.b2.onclick = self.restart

    def restart(self):
        self.running = True
        self.js.dom.b2.innerHTML = "Pause"
        self.js.dom.b2.onclick = self.stop

    def main(self):
        self.start0 = time.time()
        while True:
            if self.running:
                self.js.dom.time.innerHTML = "{:.1f}".format(time.time() - self.start0)
                time.sleep(0.5)

if __name__ == "__main__":

    httpd = Server(App, ip='0.0.0.0', verbose=False)
    print("serving at port", httpd.port)
    httpd.start()