import socket
import sys
import re
import struct
import getpass
import os


def main(serverIP):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((serverIP,10600))
    userID=input('please enter userid: ')
    #使用getpass模块获取密码
    userPwd=input('please enter password: ')
    message=userID+','+userPwd
    print(message,type(message))
    sock.send(message.encode())
    login=sock.recv(100)
    #验证是否登录成功
    if login==b'error':
        print('用户名或密码错误')
        return
    interSize=struct.calcsize('I')
    while True:
        #发送命令，接受服务器消息
        command=input('please enter command: ').lower().strip()
        #如果没有输入有效字符，则等待继续输入
        if not command:
            continue
        #向服务器发送消息
        command=''.join(command.split())
        sock.send(command.encode())
        if command in ('quit','q'):
            break
        elif command in ('list','ls','dir'):
            loc_size=struct.unpack('I',sock.recv(interSize))[0]
            files=eval(sock.recv(loc_size).decode())
            for i in files:
                print(i)
        elif ''.join(command.split())=='cd...':
            print(sock.recv(1024).decode())
        elif command in ('cwd','cd'):
            print(sock.recv(1024))
        elif command.startswith('cd'):
            print(sock.recv(1024).decode())
        elif command.startswith('get'):
            backinfo=sock.recv(1024)
            if backinfo!=b'ok':
                print(backinfo,'error 4')
            else:
                print('download.',end='')
                path='F:\\python 3.4.1'
                os.chdir(path)
                openfi=open('source.txt','wb')
                print(command.split(',')[1])
                while True:
                    print('.',end='')
                    data=sock.recv(4096)
                    if data==b'over...':
                        break
                    openfi.write(data)
                    print('okkk')
                    sock.send(b'OK')
                openfi.close()
                print('closed')

        else:
            print('invalid command.')
    sock.close()
            
    

if __name__=='__main__':
    if len(sys.argv)!=2:
        print('Usage:{0} serverIPadress'.format(sys.argv[0]))
        exit()
    serverIP=sys.argv[1]
    print(serverIP)
    #判断IP地址是否合法
    if re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$',serverIP):
        main(serverIP)
    else:
        print(' server IP adress is invalid.')
        exit()
