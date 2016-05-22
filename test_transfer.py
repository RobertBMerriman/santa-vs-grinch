from Transfer import *
import time
import threading


def listen_worker():
	listen(8888)
	while True:
		receive()

listen_thread = threading.Thread(target=listen_worker)
listen_thread.start()

time.sleep(2)

while True:
	time.sleep(1)
	send("localhost", 8888, "Wow")
	#"10.173.66.53" # Clement
	#"10.173.51.54" # Robert