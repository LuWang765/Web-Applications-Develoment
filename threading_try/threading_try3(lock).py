import threading



class mythread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global x
        #obtain lock, enter the critical region if succeeded.
        lock.acquire()
        x=x+3
        print(x)
        lock.release()

lock=threading.RLock()

t1=[]
for i in range(10):
    t=mythread()
    t1.append(t)

x=0

for i in t1:
    i.start()

