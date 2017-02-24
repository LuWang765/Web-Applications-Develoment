import socket
import threading
import time


activeDegree=dict()
flag=1

def main():
    global activeDegree
    global flag
    #obtain the IP adress of current computer
    HOST=socket.gethostbyname(socket.gethostname())

    #creak original socket suitable for windows system
    s=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    s.bind((HOST,0))

    #setting trapped data packet including IP packet
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)

    #starting intermix mode, trapping all data packets
    s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    #trapping data packets
    while flag:
        c=s.recvfrom(65565)
        host=c[1][0]
        activeDegree[host]=activeDegree.get(host,0)+1

        if c[1][0]!='**Your local ip adress':
            print (c)

    s.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
    s.close()

t=threading.Thread(target=main)
t.start()
time.sleep(60)
flag=0
t.join()
for item in activeDegree.items():
    print(item)

    
