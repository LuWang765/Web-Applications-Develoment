from threading import Thread
import time


def func1(x,y):
    for i in range(x,y):
        print ('the number is:',i)
    print ()
    time.sleep(10)

t1=Thread(target=func1,args=(15,20))
print ('t1:',t1.isAlive())
t1.start()
print ('t1:',t1.isAlive())
t1.join(20)
print ('t1:',t1.isAlive())
t2=Thread(target=func1,args=(1,5))
t2.start()
