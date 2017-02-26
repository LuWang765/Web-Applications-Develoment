from multiprocessing import Process
import os


def ni(name):
    print('module name: ',__name__)
    print('parent process: ',os.getppid())
    print('process id: ', os.getpid())
    print('hello',name)

if __name__=='__main__':
    p=Process(target=ni,args=('bob',))
    p.start()
    p.join()
