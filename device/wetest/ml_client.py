#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import json
import time, logging, base64
from httptools.remote_connection import RemoteConnection,Method
from local_config import ML_SERVER_URL
from .actions import ClickAction,loads
from common.wetest_exceptions import *

logger=logging.getLogger(__name__)

class TestType(object):
    STANDARD_TEST=0 #标准兼容测试

class Command(object):
    GET_ACTION=(Method.POST,"action/normal")
    REQUEST_OCR=(Method.POST,"action/ocr")
    REPORT_ACTION=(Method.POST,"action/update")
    START_SESSION=(Method.POST,"start/session")
    END_SESSION=(Method.POST,"end/session")
    REPORT_IMAGE = (Method.POST, "image/report")


class MlClient(object):
    def __init__(self,testid,deviceid,package,version):
        self.client=RemoteConnection(ML_SERVER_URL,keep_alive=True,timeout=4)
        self.index=0
        self.testid=testid
        self.deviceid=deviceid
        self.package=package
        self.version=version

    def _check_response(self, response):
        """
            平台正确与否通过errorcode来体现，0表示正确
        :param response:
        :return:
        """
        if not response:
            raise WeTestPlatormError("None response")

        if isinstance(response, bool):
            return response

        if not isinstance(response, dict):
            invaild_response = "Invaild response : {0}".format(response)
            raise WeTestPlatormError(invaild_response)

        error_code = response.get("status", 0)
        if error_code == 0:
            return response.get("data", True)  # 如果没有数据，还是会返回，只是不再会有data数据
        else:
            errorMessage = response.get("errorMsg", "platorm api error")
            raise WeTestPlatormError(errorMessage)

    def excute_request(self, command, params=None):
        """
            如果返回的errorcode为0，没有"data"则返回True，如果data中有数据则返回
        :param command:
        :param params:
        :return:
        """
        #platform_client = RemoteConnection(self.url, keep_alive=False)
        start_time = time.time()
        if not isinstance(command, tuple):
            raise WeTestInvaildArg("command is invaild")

        if command[0] == Method.GET:
            response = self.client.get(command[1], params)
        else:
            response = self.client.post(command[1], params)
        end_time = time.time()
        logger.debug("Command: {0} Response: {1} time: {2}s".format(command, response, (end_time - start_time)))
        response = self._check_response(response)
        return response

    def _add_basic_info(self,params):
        params["testid"]=self.testid
        params["deviceid"]=self.deviceid
        params["package"]=self.package
        params["version"]=self.version

    def get_action(self,fingerprint,width,height,threshold=5):
        """
            截图，并且返回操作节点

            ps：客户端保持上一次的操作状态更加容易。服务端维护多个手机状态，更加麻烦
        :param image_hash: 图片hash指纹
        :param last_action: 上一次的操作
        :param index:手机截图序列号
        :return:该界面下可操作的候选点集合
        """
        params={
            "fingerprint":fingerprint,
            "threshold":threshold,
            "width":width,
            "height":height
        }
        self._add_basic_info(params)
        response=self.excute_request(Command.GET_ACTION,params)
        return response

    def report_action(self, pre_fingerprint, current_fingerprint,last_action, vaild):
        """
        上报上个action是否有效
        :param pre:操作前界面的hash值{"fingerprint":12312,"seq":0}
        :param current:操作后界面的hash值
        :param image_index:上传图片的index,后台可以通过拼接获取图片url
        :param last_action:操作
        :param vaild:界面是否发生了变化
        :return:
        """
        params = {"pre":pre_fingerprint, "current":current_fingerprint, "action":last_action, "vaild":vaild}
        self._add_basic_info(params)
        response = self.excute_request(Command.REPORT_ACTION, params)
        return response

    def report_image(self, image_hash, image_index):
        params = {"fingerprint":image_hash,"seq":image_index}
        self._add_basic_info(params)
        response = self.excute_request(Command.REPORT_IMAGE, params)
        return response

    def request_ocr(self, image, image_hash, rotation):
        params = {
            "image":base64.b64encode(image).rstrip().decode('utf-8'),
            "image_hash":image_hash,
            "rotation":rotation
        }
        self._add_basic_info(params)
        response = self.excute_request(Command.REQUEST_OCR, params)
        return response


    def start_session(self,screen_width,screen_height,type=TestType.STANDARD_TEST):
        """
            开启会话。

            ps:为什么要有会话概念
            1、利于后面的分布式部署
            2、图片处理和决策必须得知道，这次测试几时结束。有结束必须要有开始
            3、屏幕长宽、版本号、包名必须有，且可以一次传输
        :param testid:
        :param deviceid:
        :param package_name:
        :param screen_width:
        :param screen_height:
        :param version:
        :param type:
        :return:
        """
        params={
            "testid":self.testid,
            "deviceid":self.deviceid,
            "package":self.package,
            "width":screen_width,
            "height":screen_height,
            "version":self.version,
            "type":type
        }
        self._add_basic_info(params)
        res=self.excute_request(Command.START_SESSION,params)

    def close_session(self):
        params={}
        self._add_basic_info(params)
        res=self.excute_request(Command.END_SESSION,params)








