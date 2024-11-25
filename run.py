"""Starts the Flask app. Is run by the exe"""
#import os
#import sys
import webbrowser
import threading
from threading import Timer
from flask import Flask
from routes import routes
from monitor_heartbeat import monitor_heartbeat

#Fix for pyinstaller compatibility with Flask
#if getattr(sys, 'frozen', False):
#    template_folder = os.path.join(sys._MEIPASS, 'templates')
#    static_folder = os.path.join(sys._MEIPASS, 'static')
 #   app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
#else:
#    app = Flask(__name__)

app = Flask(__name__)
app.register_blueprint(routes)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == "__main__":
    Timer(1, open_browser).start()
    threading.Thread(target=monitor_heartbeat, daemon=True).start()
    app.run()