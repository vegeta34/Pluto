# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import json
import math
import logging
import uiautomator.uiautomator_manager as manager
from imagetools.image_config import Color

logger = logging.getLogger(__name__)

device_width = 0
device_height = 0
device_index = 0
device_uiauto = manager.get_uiautomator()


def get_device_screen_size():
    global device_width, device_height
    if device_index % 10 == 0:
        info = device_uiauto.info
        device_width = info["displayWidth"]
        device_height = info["displayHeight"]
    return device_width, device_height


class ActionSource(object):
    OCR = 1  # 来自图片ocr识别出来的文字位置
    RANDOM = 0  # 随机点击
    ORE = 2  # 其他设备探索出来的操作
    LOCALRANDOM = 10  # 本地随机


class Action(dict):
    def __init__(self, _width, _heigth, _interval, _source, _type):
        super(Action, self).__init__()
        self["width"] = _width
        self["height"] = _heigth
        self["interval"] = _interval
        self["source"] = _source
        self["type"] = _type

    def action(self):
        """
            直接执行动作
        :return:
        """
        pass


class ClickAction(Action):
    """
        点击相关坐标
    """

    def __init__(self, x, y, width, height, interval, source):
        super(ClickAction, self).__init__(width, height, interval, source, self.__class__.__name__)
        self["x"] = x
        self["y"] = y

        self.width, self.height = get_device_screen_size()
        self.target_x = self["x"]
        self.target_y = self["y"]
        if self["source"] == ActionSource.RANDOM:
            if self.width > self.height:
                self.target_x = self.width * self["y"] / self["height"]
                self.target_y = self.height * self["x"] / self["width"]
            else:
                self.target_x = self.width * self["x"] / self["width"]
                self.target_y = self.height * self["y"] / self["height"]
            # 如果是服务器下发的随机，则需要进行回填操作。
            self["x"] = self.target_x
            self["y"] = self.target_y
            self["width"] = self.width
            self["height"] = self.height
        elif self["source"] == ActionSource.LOCALRANDOM:
            self["source"] = ActionSource.RANDOM
        else:
            self.target_x = self.width * self["x"] / self["width"]
            self.target_y = self.height * self["y"] / self["height"]

    def action(self):
        logger.info("click: {0},{1}".format(self.target_x, self.target_y))
        device_uiauto.click(self.target_x, self.target_y)

    def unified(self, rotation):
        """
        返回高为640的点击位置
        :return:
        """
        logger.info("unify")
        image_height = 640.0
        image_width = None
        if self.width > self.height:
            image_width = image_height * self.height / self.width
        else:
            image_width = image_height * self.width / self.height
        x, y = 0, 0
        if rotation == 0:
            x = self.target_x
            y = self.target_y
        elif rotation == 1:
            x = self.height - self.target_y
            y = self.target_x
        elif rotation == 2:
            x = self.width - self.target_x
            y = self.height - self.target_y
        else:
            x = self.target_y
            y = self.width - self.target_x

        x *= (image_width / min(self.width, self.height))
        y *= (image_height / max(self.width, self.height))

        tag_color = Color.RED
        if self["source"] == ActionSource.ORE:
            tag_color = Color.REDSPECIAL

        return int(x), int(y), tag_color


def _object_decoder(obj):
    if 'type' in obj and (obj['type'] == 'ClickAction' or obj['type'] == 0):
        return ClickAction(obj['x'], obj['y'], obj['width'], obj['height'], obj['interval'], obj['source'])
    return obj


def loads(obj):
    try:
        res = json.loads(obj, object_hook=_object_decoder)
        return res
    except Exception as e:
        message = "Parese to action error ==>{0}".format(obj)
        logger.exception(message)
        return None


if __name__ == '__main__':
    test = []
    c = ClickAction(100, 200, 1280, 720, 3, ActionSource.RANDOM)
    d = ClickAction(200, 400, 1280, 720, 4, ActionSource.RANDOM)
    print d.unified()
    test.append(c)
    test.append(d)
    res = json.dumps(test)
    r = loads(res)
    print r
