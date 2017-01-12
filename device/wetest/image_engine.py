# -*- coding: UTF-8 -*-
__author__ = 'alexkan'

import os, time, random, traceback
from wetest.device import *
from wetest.ml_client import *
from wetest.actions import *
from imagetools.image_check import *
from imagetools.image_upload import *

class ImageEngine(object):
    def __init__(self, width, height):
        self.device = get_device()
        self.testid = os.getenv("TESTID","203106")
        self.deviceid = os.getenv("DEVICEID", "10909")
        self.package = self.device.package
        self.version = "1.0.0"
        self.cloudscreen = self.device.cloudscreen
        self.width, self.height = width, height #self.device.get_displaysize()
        if self.width > self.height:
            self.width, self.height = self.height, self.width
        self.image_hash = None
        self.last_image_hash = None
        self.current_image_hash = None
        self.ml_client = MlClient(self.testid, self.deviceid, self.package, self.version)
        self.last_image_index = -1 # ml探索时向服务器汇报上一次截图的index，供服务器端拼接成url获取图片
        self.index = -1
        self.actions = [] #当前界面服务器返回的候选点
        self.image_check = get_image_check()


    # def takeshot(self,point=None,tag_color=Color.RED):
    #     """
    #         单纯的从cloudscreen截图。
    #     """
    #     image_data,time_inner = self.cloudscreen.takeshot()
    #     self.cloudscreen.upload_image(image_data, point, False, tag_color, time_inner)
    #     return image_data

    def analyze(self, last_action, has_login=False):
        """
        向决策服务器上报上次操作的结果。
        根据上次操作页面的结果决定是否向服务器请求获取参考操作点。
        页面发生变化时一定请求。
        页面未发生变化时则判断这个页面服务器返回的参考action是否探索完，探索完则请求。
        :param last_action: 上次操作的action
        :return:
        """
        image_data = None
        timestamp = time.time() * 1000
        rotation = 0
        issame = False
        try:
            self.last_image_hash = self.current_image_hash
            width, height = self.device.get_displaysize()
            rotation=self.device.get_rotation()
            image_data, timestamp = self.cloudscreen.takeshot()
            issame, self.current_image_hash = self.image_check.image_check(image_data)
            # 1、判断操作前后页面是否相同
            # 2、向服务器report操作结果
            if last_action and (has_login or not issame or last_action["source"] != ActionSource.RANDOM):
                # 上报
                if last_action["source"] == ActionSource.RANDOM:
                    last_action["source"] = ActionSource.ORE
                self.ml_client.report_action(self.last_image_hash, self.current_image_hash,last_action, has_login or not issame) #has_login主要是因为有些登录返回后界面未能立即发生变化
                # 上报上一张图片的index(为什么不放在report_action里面：标记红点和请求actions时序不对，只能告知服务器上一张图片的情况)
                if has_login or not issame:
                    self.ml_client.report_image(self.last_image_hash, self.last_image_index)
            # 如果界面没有发生变化 and 还有未探索的点
            if not issame or len(self.actions) == 0:
                response = self.ml_client.get_action(self.current_image_hash,width,height)
                if response["need_ocr"]:
                    # 请求OCR接口
                    # 获取屏幕旋转方向
                    rotation = self.device.get_rotation()
                    self.actions = loads(json.dumps(self.ml_client.request_ocr(image_data, self.current_image_hash, rotation)))
                else:
                    self.actions = loads(json.dumps(response["actions"]))
                    logger.info("Get Actions: {0}".format(self.actions))
            # 随机选择并删除
            image_action = self.actions.pop()
        except:
            stack = traceback.format_exc()
            logger.error(stack)
            #发生异常时本地随机，最差的情况就和现在的标准兼容一样，随机点击。
            width, height = self.device.get_displaysize()
            x = random.randint(5, width-5)
            y = random.randint(10, height - 10)
            image_action = ClickAction(x, y, width, height, 2, ActionSource.LOCALRANDOM)
        logger.info("Image Engine Return: {0}".format(image_action))
        # 根据image_action标记红点并上传上一次的截图
        x,y,color = image_action.unified(rotation)
        self.last_image_index = self.cloudscreen.upload_image(image_data, (x,y),issame,color,8, timestamp)
        return image_action

    def start_session(self):
        try:
            self.ml_client.start_session(self.width, self.height, TestType.STANDARD_TEST)
        except:
            logger.error("start session error")

    def end_session(self):
        self.ml_client.close_session()


def get_image_engine(width=1080, height=1920):
    if not get_image_engine.instance:
        get_image_engine.instance = ImageEngine(width, height)
    return get_image_engine.instance

get_image_engine.instance = None





