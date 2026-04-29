import threading
import time
import datetime

def loop():
    current = datetime.datetime.now()
    duration = 30 * 24 * 60 * 60

    print(current)

loop()
