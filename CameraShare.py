import time
from vidstream import *
import threading
import sys

receive = StreamingServer('192.168.0.131', 9999)
sending = CameraClient('192.168.0.139', 9999)

t1 = threading.Thread(target=receive.start_server())
t1.start()

time.sleep(2)

t2 = threading.Thread(target=sending.start_stream())
t2.start()

while input("") != 'stop':
    continue

receive.stop_server()
sending.stop_stream()