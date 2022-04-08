from queue import Queue

dq = Queue()

try:
    temp = dq.get_nowait()
except:
    print("empty")