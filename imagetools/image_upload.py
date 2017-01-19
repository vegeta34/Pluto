# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'

import cv2
import numpy as np
import traceback
import binascii

import os
from common import logger_config
from server_config import *
from image_tools import *
from imagetools.image_check import *

from local_config import local_image_save_path
logger = logger_config.get_logger()

buffer_len = 1024*1024

class ImageUpload(object):

    def __init__(self, _testid, _deviceid):
        self.image_index = 1
        self.info_server = get_info_server()
        self.image_server = get_image_server()
        self.last_image_issue=ImageErrorCode.NORMAL

        if type(_testid) == type(0) :
            self.testid = _testid
        elif type(_testid) == type(""):
            try:
                self.testid = int(_testid)
            except:
                logger.error("testid is error: {0}".format(_testid))
                self.testid = 0
        if type(_deviceid) == type(0):
            self.deviceid = _deviceid
        elif type(_deviceid) == type(""):
            try:
                self.deviceid = int(_deviceid)
            except:
                logger.error("deviceid is error: {0}".format(_deviceid))
                self.deviceid = 0
        self.local_image_path = "./screen_images/"
        logger.debug("testid:{0}[type:{1}], deviceid:{2}[type:{3}]".format(self.testid, type(self.testid), self.deviceid, type(self.deviceid)))

    def set_image_index(self, _image_index):
        self.image_index = _image_index

    def set_local_image_path(self, path=local_image_save_path):
        """
            设置本地测试时图片存储路径， 默认为 ./screen_images/
        :param path:  设置本地测试时图片存储路径
        :return:
        """
        self.local_image_path = path

    def __get_image_index(self):
        self.image_index += 1
        return self.image_index

    def __back_image_index(self):
        self.image_index -= 1
        return self.image_index

    def _upload_image(self, image_data, point=None, tag_color=Color.RED,  radius=8, time_stamp = time.time() * 1000):
        try:
            # 创建请求包对象
            cspkg = CsPkg()
            cspkg.Head.Cmd = CMD_UPLOAD_TEST_IMG_WITH_TESTID_REQ
            cspkg.Head.Result = 0
            cspkg.Head.DeviceID = self.deviceid

            # 创建图片上传请求体
            upload_test_img_with_testid_req = UploadTestImgWithTestIDReq()
            upload_test_img_with_testid_req.TestID = self.testid
            upload_test_img_with_testid_req.Index = self.__get_image_index()
            upload_test_img_with_testid_req.Timestamp = time_stamp

            # 处理图片
            image = image_data
            if point:
                logger.debug("mark image position = {0}".format(point))
                image_point_tag(image, point, tag_color, radius)
            image = image_encode(image, ".jpg")

            # 处理图片上传请求
            upload_test_img_with_testid_req.Image.Len = image[1].size
            upload_test_img_with_testid_req.Image.Data = image[1]

            cspkg.Body.UploadTestImgWithTestIDReq = upload_test_img_with_testid_req

            send_buffer = bytearray(buffer_len)
            bl = cspkg.pack(send_buffer, 1)

            send_buffer = send_buffer[:bl + 1]
            # print binascii.hexlify(send_buffer)

            # 连接图片上传的目标服务器
            socket_client = get_socket_client(self.image_server.ip, self.image_server.port)
            socket_client.send_data(send_buffer)
            socket_client.close()

            logger.info("Upload Image Succ ! testid:{0}, deviceid:{1}, index:{2} timestamp:{3}".format(self.testid, self.deviceid,
                                                                                          self.image_index, time_stamp))
            return self.image_index
        except:
            logger.error("Upload Image Error! testid:{0}, deviceid:{1}, index:{2}".format(self.testid, self.deviceid,
                                                                                          self.image_index))
            stack = traceback.format_exc()
            logger.error(stack)
            return -1

    def _report_ui_issue(self, image_data,time_stamp,image_index,issame=False):
        socket_client=None
        current_type=ImageErrorCode.NORMAL
        try:
            # 创建请求包对象

            if image_data is None:
                return

            current_type=check_black_white(image_data)
            if self.last_image_issue is not ImageErrorCode.NORMAL and self.last_image_issue == current_type:
                #判断两次连续两张图片是否都是黑图或者白图
                cspkg = CsPkg()
                cspkg.Head.Cmd = CMD_UPLOAD_ERROR_INFO_REQ
                cspkg.Head.Result = 0
                cspkg.Head.DeviceID = self.deviceid

                upload_error_info_req = UploadErrorInfoReq()
                upload_error_info_req.Code=ERR_UI
                upload_error_info_req.Level=ERR_NORMAL
                upload_error_info_req.Time=time_stamp

                if current_type==ImageErrorCode.BLACK:
                    upload_error_info_req.Desc="界面出现黑屏"
                elif current_type==ImageErrorCode.WHITE:
                    upload_error_info_req.Desc="界面出现白屏"


                cspkg.Body.UploadErrorInfoReq=upload_error_info_req

                logger.debug("report ui issue body = {0}".format(upload_error_info_req))

                send_buffer = bytearray(buffer_len)
                bl = cspkg.pack(send_buffer, 1)

                send_buffer = send_buffer[:bl + 1]

                # 连接info server服务器
                socket_client = get_socket_client(self.info_server.ip, self.info_server.port)
                socket_client.send_data(send_buffer)

                recv_buffer = socket_client.recv_data(buffer_len)

                m_cspkg = CsPkg()
                m_cspkg.unpack(recv_buffer, buffer_len)

                cmd = m_cspkg.Head.Cmd
                if cmd == CMD_UPLOAD_ERROR_INFO_RES and m_cspkg.Head.Result == 0:
                    logger.debug("report ui issue success")
                else:
                    logger.error("Can not report ui issue. error code = {0}".format(m_cspkg.Head.Result))
            if issame:
                cspkg = CsPkg()
                cspkg.Head.Cmd = CMD_REPORT_UI_ISSUE_REQ
                cspkg.Head.Result = 0
                cspkg.Head.DeviceID = self.deviceid

                report_ui_issue_req = ReportUIIssueReq()
                report_ui_issue_req.IssueType = ImageErrorCode.IMAGE_SIMILAR
                report_ui_issue_req.Index = image_index
                report_ui_issue_req.time = time_stamp

                cspkg.Body.ReportUIIssueReq = report_ui_issue_req

                logger.debug("report ui issue body = {0}".format(report_ui_issue_req))

                send_buffer = bytearray(buffer_len)
                bl = cspkg.pack(send_buffer, 1)

                send_buffer = send_buffer[:bl + 1]

                # 连接info server服务器
                socket_client = get_socket_client(self.info_server.ip, self.info_server.port)
                socket_client.send_data(send_buffer)

                recv_buffer = socket_client.recv_data(buffer_len)

                m_cspkg = CsPkg()
                m_cspkg.unpack(recv_buffer, buffer_len)

                cmd = m_cspkg.Head.Cmd
                if cmd == CMD_REPORT_UI_ISSUE_RES and m_cspkg.Head.Result == 0:
                    logger.debug("report ui issue success")
                else:
                    logger.error("Can not report ui issue. error code = {0}".format(m_cspkg.Head.Result))

        except:
            logger.exception("Report ui issue error")
        finally:
            if socket_client:
                socket_client.close()
        self.last_image_issue=current_type



    def _save2localdirectory(self, image, path, point=None, tag_color=Color.RED,  radius=8):
        # 处理图片
        try :
            if point:
                image_point_tag(image, point, tag_color, radius)
            if not os.path.exists(path):
                os.makedirs(path)

            local_full_path = path + str(self.__get_image_index()) + ".jpg"

            image_save(image, local_full_path)
            logger.info("Save Image Succ ! testid:{0}, deviceid:{1}, index:{2}, path: {3}".format(self.testid, self.deviceid,
                                                                                         self.image_index, local_full_path))
            return self.image_index
        except :
            logger.error("Save Image Error! testid:{0}, deviceid:{1}, index:{2}".format(self.testid, self.deviceid,
                                                                                          self.image_index))
            stack = traceback.format_exc()
            logger.error(stack)
            return -1

    def upload_image(self, image, point, issame=None,tag_color=Color.RED,  radius=8, time_stamp = time.time() * 1000):
        """

        :param image:  内存图片
        :param point:  标记点
        :param tag_color:  标记颜色，默认红色
        :param radius:  标记点半径，默认半径8像素
        :return: 执行结果
        """
        # 预处理图片， 内存图片 -> opencv格式图片
        if image is None:
            logger.error("Image Data Error! No Image Data.")
            return -1
        image = np.asarray(image)
        image = cv2.imdecode(image, 1)

        env = os.environ.get("PLATFORM_IP")
        if env:
            # cloud device
            upload_status = False
            for i in range(0,3):
                image_index = self._upload_image(image, point, tag_color, radius, time_stamp)
                if image_index == -1:
                    self.__back_image_index()
                else :
                    upload_status = True
                    self._report_ui_issue(image,time_stamp, image_index,issame)
                    return image_index
            if not upload_status:
                logger.error(
                    "Upload Image Error By Retry Times! testid:{0}, deviceid:{1}, index:{2}".format(self.testid,
                                                                                                    self.deviceid,
                                                                                                    self.image_index))
        else :
            # 本地测试，图片存储在本地
            return self._save2localdirectory(image, self.local_image_path, point, tag_color, radius)

    def data_save(self, data, file_path):
        data_write(data,file_path)



if __name__ == "__main__":
    # a = open("./images_tempfile/wetest.jpg", "rb")
    # b = a.read()
    # b = np.array(b)
    # a.close()
    # m = cv2.CV_LOAD_IMAGE_COLOR
    # b = cv2.imdecode(b, 0)
    # pass
    image_upload = ImageUpload(203940, 11422)
    image_upload.set_image_index(10007)
    image = cv2.imread("../test/images_tempfile/black.jpg")
    time_stamp = time.time() * 1000
    #image_upload._upload_image(image, (50, 50), Color.RED, 6, time_stamp)
    image_upload._report_ui_issue(image, time_stamp)
