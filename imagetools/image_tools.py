# -*- coding: UTF-8 -*-
"""
图像相似度检测
"""
__author__ = 'guoruihe'

import numpy as np
import cv2
import logging
import time

from image_config import *

logger=logging.getLogger(__name__)

BLACK_THRESHOLD = 240
WHITE_THRESHOLD = 20

def image_similar_check(image_org_path, image_des_path, distance=5, hash_type='dhash'):
    """

    :param image_org_path: 图片1路径(前次图片)
    :param image_des_path: 图片2路径(当前图片)
    :param distance: hamming距离阈值
    :param hash_type: 指纹算法, ahash、dhash、phash。
    :return: 是否相似
    """
    image_org = cv2.imread(image_org_path)
    image_des = cv2.imread(image_des_path)
    hamming_dis = 0
    if hash_type == 'dhash':
        hamming_dis = compare_image_dhash(image_org, image_des)
    elif hash_type == 'ahash':
        hamming_dis = compare_image_ahash(image_org, image_des)
    elif hash_type == 'phash':
        hamming_dis = compare_image_phash(image_org, image_des)
    else:
        print "Unknow hash type. Use default dhash to calculate."
        hamming_dis = compare_image_dhash()

    if hamming_dis <= distance:
        return True
    else:
        return False


def get_image_fingerprint(image_path, hash_type='dhash'):
    """
    计算图像指纹
    :param image_path: 图片路径
    :param hash_type: 指纹算法, ahash、dhash、phash。
    :return: 图片指纹
    """
    image = cv2.imread(image_path)
    if hash_type == 'dhash':
        return get_image_dhash(image)
    elif hash_type == 'ahash':
        return get_image_ahash(image)
    elif hash_type == 'phash':
        return get_phash(image)
    else:
        print "Unknow hash type. Use default dhash to calculate."
        return get_image_dhash(image)


def hamming_distance(hash1,hash2):
    """
    计算hamming距离
    :param hash1:
    :param hash2:
    :return: hamming距离
    """

    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num


def cal_hash(image):
    """
    获取图像的平均值hash值，图像为灰度图像。
    :param image:
    :return:
    """

    avreage = np.mean(image)
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] > avreage:
                hash.append('1')
            else:
                hash.append('0')
    return "".join(hash)


def get_image_ahash(image, row=8, col=8):
    image = cv2.resize(image, (row, col))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hash = cal_hash(gray)
    return hash


def compare_image_ahash(image_org, image_des):
    hash_org = get_image_ahash(image_org)
    hash_des = get_image_ahash(image_des)
    return hamming_distance(hash_org,hash_des), hash_des


def cal_dhash(image):
    """
    获取图像的差异值hash，图像为灰度图像。
    :param image:
    :return:
    """

    hash = []
    for i in range(image.shape[0]):
        for j in range(1,image.shape[1]):
            if image[i,j-1] > image[i,j]:
                hash.append('1')
            else:
                hash.append('0')
    return "".join(hash)


def get_image_dhash(image, row=9, col=8):
    """
    计算图片的dhash值。
    dhash：resize to 9:8 -> cvt -> dhash
    :param image: 图片
    :param row: 行数，默认9
    :param col: 列数，默认8
    :return: 图片dhash值
    """

    image = cv2.resize(image, (row, col))
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hash = cal_dhash(image)
    return hash


def compare_image_dhash(image_org, image_des, row=9, col=8):
    """
    通过dhash算法，比较两张图片的指纹是否一致，完成图片相似性检测
    :param image_org: 原始图片
    :param image_des: 待比较图片
    :param row: dhash缩放后的行数
    :param col: dhash缩放后的列数
    :return: 两张图片之间的hamming距离
    """

    hash_org = get_image_dhash(image_org, row, col)
    hash_des = get_image_dhash(image_des, row, col)
    return hamming_distance(hash_org, hash_des), hash_des


def get_phash(image, cell=1):
    """
    计算图片的感知hash。
    phash: resize to 32n * 32n -> cvt -> dct -> hash。
    :param image:图片
    :param cell: 32*32单元数为cell*cell
    :return: 图片的phash
    """
    image = cv2.resize(image, (32*cell, 32*cell))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # 取左上角的8*8，这些代表图片的最低频率
    # 这个操作等价于c++中利用opencv实现的掩码操作
    # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
    dct_roi = dct[0:8*cell, 0:8*cell]
    hash = cal_hash(dct_roi)
    return hash


def compare_image_phash(image_org, image_des, cell=1):

    hash_org = get_phash(image_org, cell)
    hash_des = get_phash(image_des, cell)
    return hamming_distance(hash_org,hash_des), hash_des


def image_resize(image, target_height=600):
    """
        缩放图像尺寸，将高度缩放至指定高度，宽度按照比例变换
    :param image:  待缩放的图像
    :param target_height: 目标高度
    :return: 缩放后的图片
    """
    (width, height, dimension) = image.shape
    width = width * target_height / height
    image = cv2.resize(image, (width, target_height))
    return image


def image_point_tag(image, point, tag_color=Color.RED,  radius=8):
    image_org = image.copy()
    cv2.circle(image_org, point, radius, tag_color, radius * 2)
    cv2.addWeighted(image_org, 0.5, image, 0.5, 0, image)


def image_save(image, path):
    cv2.imwrite(path, image)


def image_encode(image, img_format):
    """

    :param image: 图像数据
    :param img_format: 图像格式，.jpg .png
    :return:
    """
    return cv2.imencode(img_format, image)


def data_write(data, path):
    file = open(path, "wb")
    file.write(data)
    file.close()
    return True


def image_gray_level_calu(image):
    (width, height, dimension) = image.shape


def check_black_white2(image):
    (width, height, dimension) = image.shape
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # BGR 转到 HSV 空间
    lower_black = np.array(HSVColor.BLACK_LOWER)
    upper_black = np.array(HSVColor.BLACK_UPPER)
    mask = cv2.inRange(hsv, lower_black, upper_black)
    ret, binary = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        areas = np.zeros( len(contours))
        idx = 0
        for contour in contours:
            areas[idx] = cv2.contourArea(contour)
            idx += 1
        areas_sorted = cv2.sortIdx(areas, cv2.SORT_DESCENDING | cv2.SORT_EVERY_COLUMN)
        black_percent = areas[areas_sorted[0]] / (width * height)
        logger.debug("Black percent = {0}".format(black_percent))
        if black_percent[0] > BLACK_IMAGE_PERCENT:
            logger.debug("image is black")
            return ImageErrorCode.BLACK

    lower_white = np.array(HSVColor.WHITE_LOWER)
    upper_white = np.array(HSVColor.WHITE_UPPER)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    ret, binary = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        areas = np.zeros(len(contours))
        idx = 0
        for contour in contours:
            areas[idx] = cv2.contourArea(contour)
            idx += 1
        areas_sorted = cv2.sortIdx(areas, cv2.SORT_DESCENDING | cv2.SORT_EVERY_COLUMN)
        white_percent = areas[areas_sorted[0]] / (width * height)
        logger.debug("White percent = {0}".format(white_percent))
        if white_percent[0] > WHITE_IMAGE_PERCENT:
            logger.debug("image is white")
            return ImageErrorCode.WHITE

    return ImageErrorCode.NORMAL


def check_black_white(image):
    upper_black = np.array(RGBColor.BLACK_UPPER)
    black_count = (image <= upper_black).sum()
    black_percent = np.float(black_count)/image.size
    logger.debug("Black percent = {0}".format(black_percent))
    if black_percent > 0.95:
        return ImageErrorCode.BLACK
    # lower_white = np.array(RGBColor.WHITE_LOWER)
    # white_count = (image >= lower_white).sum()
    # white_percent = np.float(white_count) / image.size
    # if white_percent > 0.95:
    #     return ImageErrorCode.WHITE
    return ImageErrorCode.NORMAL


if __name__ == '__main__':
    image_data = cv2.imread('../test/images_tempfile/white.jpg')
    start_time = time.time()
    print check_black_white(image_data)
    end_time = time.time()
    print end_time - start_time
    # print image_data.shape
    # img = cv2.imencode(".jpg", image_data)
    # image_data = image_resize(image_data, 600)
    # image_point_tag(image_data, (200, 200))
    # image_save(image_data, "./images_tempfile/600.jpg");
    # image_similar_check('5.jpg', '4.jpg')
    pass
