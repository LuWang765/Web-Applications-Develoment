import threading
from random import randint
from time import sleep


class Producer(threading.Thread):
    def __init__(self,threadname):
        threading.Thread.__init__(self,name=threadname)
    def run(self):
        global x
        while True:
            #obtain lock
            con.acquire()
            # accomodate 20 elements
            if len(x)==20:
                con.wait()
                print('Producer is waiting...')
            else:
                print('Producer: ',end='')
                #create new element
                x.append(randint(1,1000))
                print(x)
                sleep(1)

                con.notify()
            con.release()

class Consumer(threading.Thread):
    def __init__(self,threadname):
        threading.Thread.__init__(self,name=threadname)
    def run(self):
        global x

        while True:
            con.acquire()
            if not x:
                con.wait()
                print('Consumer is waiting...')
            else:
                print(x.pop(0))
                print(x)
                sleep(2)
                con.notify()
            con.release()

#create Condition object and thread of producer and consumer
con=threading.Condition()
x=[]
p=Producer('Producer')
c=Consumer('Consumer')
p.start()
c.start()
p.join()
c.join()
