#-*- coding: UTF-8 -*-
__author__ = 'alexkan,minhuaxu'

import json, socket, struct, time
from common.wetest_exceptions import *


class SocketClient(object):

    def __init__(self, _host='localhost', _port=8080):
        self.host = _host
        self.port = _port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(6) #设置超时
        self.socket.connect((self.host, self.port))

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_data(self, data):
        self.socket.sendall(data)

    def recv_data(self, buffer_len):
        view = memoryview(bytearray(buffer_len))
        recv_size = self.socket.recv_into(view[0:], buffer_len)
        # print str(view.tobytes())
        return view

    def close(self):
        self.socket.close()


def get_socket_client(host, port):
    return SocketClient(host, port)

if __name__ == "__main__":
    socket_client = get_socket_client("10.206.3.27", 8080)
    pass

