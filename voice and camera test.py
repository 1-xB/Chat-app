import time
from vidstream import *
import threading
import sys

receive = StreamingServer('192.168.0.131', 9999)
sending = CameraClient('192.168.0.139', 9999)

sending2 = AudioSender('192.168.0.139', 1111)
receive2 = AudioReceiver('192.168.0.131', 1111)

t1 = threading.Thread(target=receive.start_server())
t3 = threading.Thread(target=receive2.start_server())
t3.start()
t1.start()

time.sleep(1)
t4 = threading.Thread(target=sending2.start_stream())
t2 = threading.Thread(target=sending.start_stream())
t4.start()
t2.start()

while input("") != 'stop':
    continue

receive.stop_server()
sending.stop_stream()
sending2.stop_stream()
receive2.stop_server()