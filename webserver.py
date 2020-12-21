"""
web server 服务接口
"""
from socket import *
from select import select
import re
import os

class Handle:
    def __init__(self,connfd,html):
        self.connfd = connfd
        self.html = html
    def request(self):
        result = self.connfd.recv(1024*10).decode()
        # pattern = r"[A-Z]+\s+(/\S*)"
        data = re.findall(r"GET (/.*) HTTP/1.1",result)[0]
        if data:
            print(data)
            self.send_html(data)
        # else:
        #     response = "HTTP/1.1 404 Not Found\r\n"
        #     response += "\r\n"
        #     connfd.send(response.encode())

    def send_html(self, data):
        if data == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + data
        try:
            file = open(filename,"rb")
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "NOT FOUND"
            response = response.encode()
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response = response.encode() + file.read()
        finally:
            self.connfd.send(response)


class WebServer:
    def __init__(self, host="0.0.0.0", port=0, html=""):
        self.host = host
        self.port = port
        self.html = html
        self.rlist = []
        self.wlist = []# 创建套接字
        self.xlist = []
        self.sock = self.create_socket()

    # 创建套接字
    def create_socket(self):
        sock = socket()
        self.address = (self.host, self.port)
        sock.bind(self.address)
        sock.setblocking(False)  # 非阻塞
        return sock

    # 处理浏览器连接
    def connect(self):
        connfd, addr = self.sock.accept()
        connfd.setblocking(False)
        self.rlist.append(connfd)  # 添加浏览器

    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        self.rlist.append(self.sock)
        # IO多路复用模型
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sock:
                    self.connect()
                else:
                    self.handle = Handle(r,self.html)
                    self.handle.request()
                    self.rlist.remove(r)
                    r.close()

if __name__ == '__main__':
    # 用户如何去使用
    # 需要用户决定什么
    httpd = WebServer(host="0.0.0.0", port=7879, html="./static")
    httpd.start()  # 入口 启动服务