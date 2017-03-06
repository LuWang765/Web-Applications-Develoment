import socket
import threading
import os
import struct
import time


users={'Wang':{'pwd':'123456','home':r'f:\python 3.4.1'},'Yang':{'pwd':'654321','home':r'f:\\'}}

def server(conn,addr,home):
    print('new client: '+str(addr))

    os.chdir(home)
    while True:
        data=conn.recv(1024).decode()
        print(data,type(data))

        if data.lower() in ('quit','q'):
            break
        #查看当前文件夹的文件列表
        elif data.lower() in ('list','ls','dir'):
            files=str(os.listdir(os.getcwd()))
            files=files.encode()
            conn.send(struct.pack('I',len(files)))
            conn.send(files)
        #切换至上一级目录
        elif ''.join(data.lower().split())=='cd...':
            cwd=os.getcwd()
            newcwd=cwd[:cwd.rindex('\\')]
            if newcwd[-1]==':':
                newcwd+='\\'
            if newcwd.lower().startswith('home'):
                os.chdir(newcwd)
                conn.send(b'OK')
            else:
                conn.send(b'error 1')
        #查看当前目录
        elif data.lower() in ('cwd','cd'):
            conn.send(os.getcwd().encode())
            
        elif data.lower().startswith('cd'):
            data=data.split(maxsplit=1)
            if len(data)==2 and os.path.isdir(data[1]) and data[1]!=os.path.absdir(data[1]):
                os.chdir(data[1])
                conn.send(b'OK')
            else:
                conn.send(b'error 2')

        elif data.lower().startswith('get'):
            data=data.split(',')
            #检查文件是否存在
            if len(data)==2 and os.path.isfile(data[1]):
                conn.send(b'ok')
                fp=open(data[1],'rb')
                while True:
                    content=fp.read(4096)
                    if not content:
                        conn.send(b'over...')
                        break
                    conn.send(content)
                    time.sleep(10)
                    if conn.recv()==b'OK':
                        continue
                fp.close()
            else:
                conn.send(b'no')
        else:
            conn.send(b'invalid')

    conn.close()
    print(str(addr)+'连接关闭')
    
            
                      

if __name__=='__main__':
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('',10600))
    sock.listen(5)
    while True:
        conn,addr=sock.accept()
        userid,userpwd=conn.recv(1024).decode().split(',')
        print(userid,userpwd)
        if userid in users and users[userid]['pwd']==userpwd:
            conn.send(b'OK')
            home=users[userid]['home']
            t=threading.Thread(target=server,args=(conn,addr,home))
            t.daemon=True
            t.start()
        else:
            conn.send(b'error 3')
    
