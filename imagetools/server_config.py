# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'

from local_config import info_server_address, info_server_port, target_directory, info_server_configuration_file
from tdr.image_proto import *
from socket_client import *
import logging

logger=logging.getLogger(__name__)



class InfoServer(object):

    def __init__(self, _ip=info_server_address, _port=info_server_port):
        self.ip = _ip # 正式服10.205.2.216，预发布服10.206.3.27， 测试服10.12.234.150
        self.port = _port

    def get_info_server(self):
        return self.ip, self.port

class ImageServer(object):

    def __init__(self, _ip="", _port=0):
        self.ip = _ip
        self.port = _port

    def get_image_server(self):
        return self.ip, self.port


def get_info_server():
    if get_info_server.instance:
        return get_info_server.instance
    get_info_server.instance = InfoServer()
    return get_info_server.instance

get_info_server.instance = None


buffer_len = 1024 * 10


def get_image_server():
    if get_image_server.instance:
        return get_image_server.instance

    send_buffer = bytearray(buffer_len)

    cspkg = CsPkg()
    cspkg.Head.Cmd = CMD_ALLOC_SVR_REQ
    cspkg.Head.Result = 0

    alloc_svr_req = AllocSvrReq()
    alloc_svr_req.Type = 0
    cspkg.Body.AllocSvrReq = alloc_svr_req

    bl = cspkg.pack(send_buffer, 1)

    info_server = get_info_server()
    logger.debug("info server ip ={0}, port={1}".format(info_server.ip, info_server.port))
    socket_client = get_socket_client(info_server.ip, info_server.port)
    socket_client.send_data(send_buffer)

    recv_buffer = socket_client.recv_data(buffer_len)

    m_cspkg = CsPkg()
    m_cspkg.unpack(recv_buffer, buffer_len)

    cmd = m_cspkg.Head.Cmd
    if cmd == CMD_ALLOC_SVR_RES and m_cspkg.Head.Result == 0:
        ip = int2ip(m_cspkg.Body.AllocSvrRes.SvrIP)
        port = m_cspkg.Body.AllocSvrRes.SvrPort
        get_image_server.instance = ImageServer(ip, port)
        logger.debug("image server ip ={0}, port={1}".format(ip, port))
        return get_image_server.instance
    else:
        logger.error("Can not get image server ip:port. Please check info server.")
        return "", -1

get_image_server.instance = None


def int2ip(ip_int):
    ip = str(ip_int & 0xff) + "." + str(ip_int >> 8 & 0xff) + "." + str(ip_int >> 16 & 0xff) + "." + str(ip_int >> 24 & 0xff)
    return ip


if __name__ == "__main__":
    image_server = get_image_server()
    pass









