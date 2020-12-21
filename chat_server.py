"""
Author:张磊
Email:www.zhangzhanpo@qq.com
Time:2020-12-15
Evn:python3.6
socket and process exercise
"""
from socket import *
from multiprocessing import *
import sys
# 根据情况，创建全局变量
Host = "0.0.0.0"
PORT = 7879
ADDR = (Host, PORT)
# 存储用户信息的结构
user = {}

# 1.4根据讨论情况，创建对应功能函数
def do_login(udp_socket, name, address):
    if name in user or "管理" in name:
        udp_socket.sendto(b"Fail", address)
    else:
        list01 = []
        for key in user:
            list01.append(key)
        res = ",".join(list01)
        info = "OK %s" % res
        udp_socket.sendto(info.encode(), address)
        msg = "欢迎 %s 进入聊天室" % name
        for key, value in user.items():
            udp_socket.sendto(msg.encode(), value)
        user[name] = address


def do_chat(udp_socket, name, content):
    msg = "%s : %s" % (name, content)
    for key, value in user.items():
        if name != key:
            udp_socket.sendto(msg.encode(), value)


def do_exit(udp_socket, name):
    del user[name]
    msg = "%s 已退出聊天室" % name
    for key, value in user.items():
        udp_socket.sendto(msg.encode(), value)


# 1.搭建总体逻辑结构
def main():
    # 1.1创建udp套接字
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(ADDR)
    p = Process(target=handle,args=(udp_socket,),daemon=True)
    p.start()
    #父进程发送管理员消息
    while True:
        inform = input("管理员消息：")
        if inform == "exit":
            break
        msg = "CHAT 管理员消息 %s" % inform
        #父进程发给子进程
        udp_socket.sendto(msg.encode(),ADDR)



def handle(udp_socket):
    # 1.2循环接收用户请求
    while True:
        data, addr = udp_socket.recvfrom(1024)
        data = data.decode().split(" ", 2)
        # 1.3根据请求，分情况讨论
        if data[0] == "LOGIN":
            do_login(udp_socket, data[1], addr)
        elif data[0] == "CHAT":
            do_chat(udp_socket, data[1], data[2])
        elif data[0] == "EXIT":
            do_exit(udp_socket, data[1])


if __name__ == '__main__':
    main()  # 启动
