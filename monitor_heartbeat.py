"""Terminates app once user closes the browser tab"""
import time
import sys
import os
import signal

request_period_seconds = 1
heartbeat_timeout_seconds = 10
last_check_in_time = time.time()

def monitor_heartbeat():
    global last_check_in_time, request_period_seconds, heartbeat_timeout_seconds

    while True:
        time.sleep(request_period_seconds)
        print('heartbeat')
        if time.time() - last_check_in_time >= heartbeat_timeout_seconds:
            terminate_app()
            break

def check_in():
    global last_check_in_time

    last_check_in_time = time.time()

#Only works if it is running as exe
def terminate_app():
    if getattr(sys, 'frozen', False):
        os.kill(os.getpid(), signal.SIGTERM)
