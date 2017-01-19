# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'


class Color(object):
    """
        特殊颜色定义
    """
    RED = (0, 0, 255)  # 红色
    BLACK = (0, 0, 0)  # 黑色
    WHITE = (255, 255, 255)  # 白色
    GREEN = (0, 255, 0)  # 绿色
    BLUE = (255, 0, 0)  # 蓝色
    YELLOW = (0, 255, 255)  # 黄色
    PURPLE = (255, 0, 255)  # 紫色
    REDSPECIAL = (255, 0, 0)


class RGBColor(object):
    WHITE_LOWER = [240, 240, 240]
    BLACK_UPPER = [20, 20, 20]


class HSVColor(object):
    WHITE_LOWER = [0, 0, 221]
    WHITE_UPPER = [180, 30, 255]

    BLACK_LOWER = [0, 0, 0]
    BLACK_UPPER = [180, 255, 46]


class ImageErrorCode(object):
    NORMAL = 0
    BLACK = 1
    WHITE = 2
    BLACK_BODER = 4
    WHITE_BODER = 5
    IMAGE_SIMILAR = 8


BLACK_IMAGE_PERCENT = 0.95
WHITE_IMAGE_PERCENT = 0.95
