# -*- coding: UTF-8 -*-
__author__ = "alexkan"

import socket
class SocketClient(object):

    def __init__(self, _host='localhost', _port=4004):
        self.host = _host
        self.port = _port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.sendall(data)

    def recv(self, total):
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = self.socket.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        return view

    def close(self):
        self.socket.close()