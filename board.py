import time

def main_loop(app):
    while True:
        try:
            app.js.dom.message.innerHTML = "calendar refresh"
            time.sleep(1)
            app.js.dom.message.innerHTML = "..."
            time.sleep(15)
        except:
            pass