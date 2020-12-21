from socket import *
from multiprocessing import Process
import sys

# 根据需求，创建全局变量
# 存储服务器地址
SERVER_ADDR = ("localhost", 7879)

# 1.3编写功能函数
def do_login(udp_socket):
    while True:
        # 输入用户名发送给服务端
        name = input("请输入您的用户名：")
        msg = "LOGIN " + name
        udp_socket.sendto(msg.encode(), SERVER_ADDR)
        # 等待服务端返回结果
        data, addr = udp_socket.recvfrom(1024)
        data = data.decode().split(" ")
        if data[0] == "OK":
            print("您已进入聊天室")
            print(f"{data[1]}正在聊天室中")
            return name
        else:
            print("用户名已存在")

def receive_msg(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(1024*10)
        msg = "\n" + data.decode() + "\n发言："
        print(msg,end = "")

def send_msg(udp_socket, name):
    while True:
        try:
            content = input("发言：")
        except KeyboardInterrupt:
            content = "exit"
        if content == "exit":
            msg = "EXIT %s" % (name)
            udp_socket.sendto(msg.encode(), SERVER_ADDR)
            sys.exit("您已退出聊天室")
        else:
            msg = "CHAT %s %s" % (name, content)
            udp_socket.sendto(msg.encode(), SERVER_ADDR)

def do_chat(udp_socket, name):
    p = Process(target=receive_msg, args=(udp_socket,), daemon=True)
    p.start()
    send_msg(udp_socket, name)

def do_exit():
    pass


# 1.启动函数
def main():
    # 1.1创建udp套接字
    udp_socket = socket(AF_INET, SOCK_DGRAM)

    # 1.2创建服务端功能结构
    # 1.2.1进入聊天室
    name = do_login(udp_socket)

    # 1.2.2聊天
    do_chat(udp_socket, name)
    # 退出
    do_exit()

if __name__ == '__main__':
    main()
