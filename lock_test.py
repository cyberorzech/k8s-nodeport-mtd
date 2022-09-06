from threading import Lock

lock = Lock()
with lock:
    a = 2
    a = a + 4
    print(a)
