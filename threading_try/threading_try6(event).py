import threading


class mythread(threading.Thread):
    def __init__(self,threadname):
        threading.Thread.__init__(self,name=threadname)

    def run(self):
        global myevent

        if myevent.isSet():
            myevent.clear()
            myevent.wait()
            print (self.getName(),'set')
        else:
            print(self.getName(),'not set')

myevent=threading.Event()
myevent.set()

for i in range(10):
    t=mythread(str(i))
    t.start()
    #t.join()
