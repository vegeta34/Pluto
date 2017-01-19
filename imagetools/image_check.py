# -*- coding: UTF-8 -*-
"""
图像相似度检测
"""
__author__ = 'guoruihe'

import numpy as np
import cv2
from image_tools import *
from cloudscreen.CloudScreen import *

logger = logging.getLogger(__name__)

class ImageCheck(object):
    """
    图片相似性检测
    """

    def __init__(self):
        self.image_pre = None

    def image_check2(self, image):
        """
        传入一张图片，判断是否与前图相似，返回相似性判断结果、当前图片指纹
        :param image: 图片
        :return: 相似结果、图片指纹
        """
        if image is None:
            logger.error("Image Data Error! No Image Data.")
            return -1
        image = np.asarray(image)
        image = cv2.imdecode(image, 0)  # 0 is Gray Image, 1(cv2.CV_LOAD_IMAGE_COLOR) is Color Image
        result = False
        fingerprint = None
        if self.image_pre is None:
            result = False
            fingerprint = self.get_image_fingerprint(image)
        else:
            result, fingerprint = self._image_check_hash(image)
        self.image_pre = image
        return result, fingerprint

    def image_check(self, image):
        """
        传入一张图片，判断是否与前图相似，返回相似性判断结果、当前图片指纹
        :param image: 图片
        :return: 相似结果、图片指纹
        """
        if image is None:
            logger.error("Image Data Error! No Image Data.")
            return -1
        image = np.asarray(image)
        image = cv2.imdecode(image, 0)  # 0 is Gray Image, 1(cv2.CV_LOAD_IMAGE_COLOR) is Color Image
        if self.image_pre is None:
            result = False
            fingerprint = self.get_image_fingerprint(image)
            self.image_pre = image
            return result, fingerprint
        else:
            distance, fingerprint = self._image_check_hash(image)
        if distance <= 5:
            result = True
        else:
            # dhash太敏感，增加一些其他的检测算法
            lines = self._get_lines(image)
            pre_lines = self._get_lines(self.image_pre)
            if lines == pre_lines == 0:
                lines_percent = 1
            else:
                lines_percent = min(lines, pre_lines)*1.0/max(lines, pre_lines)
            hist = self._calc_hist(image)
            pre_hist = self._calc_hist(self.image_pre)
            logger.info("pre lines: {0} lines: {1}".format(pre_lines, lines))
            hist_result = cv2.compareHist(hist, pre_hist, cv2.cv.CV_COMP_BHATTACHARYYA)
            hist_result = 1 - hist_result
            distance_percent = (64-distance)*1.0/64
            logger.info("lines percent: {0} hist percent: {1} distance percent: {2}".format(lines_percent, hist_result, distance_percent))
            same_pre=(lines_percent + hist_result + distance_percent)/3.0
            if  same_pre> 0.92:
                result = True
            else:
                result = False
        self.image_pre = image
        return result, fingerprint

    def _get_lines(self,image):
        edges = cv2.Canny(image, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, 50, 10)
        return lines.size

    def _calc_hist(self, image):
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist).flatten()
        return hist

    def _image_check_hash(self, image, hash_type='dhash'):
        """

        :param image: 待判断图片
        :param distance: hamming距离阈值
        :param hash_type: 指纹算法, ahash、dhash、phash。
        :return: 是否相似, 当前图片指纹
        """
        if hash_type == 'dhash':
            hamming_dis, hash = compare_image_dhash(self.image_pre, image)
        elif hash_type == 'ahash':
            hamming_dis, hash = compare_image_ahash(self.image_pre, image)
        elif hash_type == 'phash':
            hamming_dis, hash = compare_image_phash(self.image_pre, image)
        else:
            logger.error("Unknow hash type. Use default dhash to calculate.")
            hamming_dis, hash = compare_image_dhash(self.image_pre, image)

        hash = self._str2long(hash)
        return hamming_dis, hash

    def get_image_fingerprint(self, image, hash_type='dhash'):
        """
        计算图像指纹
        :param image_path: 图片路径
        :param hash_type: 指纹算法, ahash、dhash、phash。
        :return: 图片指纹
        """
        hash = None
        if hash_type == 'dhash':
            hash = get_image_dhash(image)
        elif hash_type == 'ahash':
            hash = get_image_ahash(image)
        elif hash_type == 'phash':
            hash = get_phash(image)
        else:
            logger.error("Unknow hash type. Use default dhash to calculate.")
            hash = get_image_dhash(image)
        hash = self._str2long(hash)

        return hash

    def _str2long(self, str_bit_64):
        res = 0
        if len(str_bit_64) != 64:
            return 0
        for i in range(64):
            res *=2
            if str_bit_64[i] == '1':
                res += 1
        return res

def get_image_check():
    if get_image_check.instance:
        return get_image_check.instance
    get_image_check.instance = ImageCheck()
    return get_image_check.instance


get_image_check.instance = None



if __name__ == '__main__':
    image_check = ImageCheck()
    # res = image_check.str2long('1111111100000000111111110000000011111111000000001111111100000000')
    # print res
    # print bin(res)
    # cloudscreen = get_cloudscreen()
    # for i in range(2):
    #     image_data = cloudscreen.takeshot()
    #     # image = cv2.imread('../images/' + str(i) + ".jpg")
    #     result, fingerprint = image_check.image_check(image_data)
    #     time.sleep(2)
    #     image_data = cloudscreen.takeshot()
    #     result, fingerprint = image_check.image_check(image_data)
    #     print result, 'fingerprint : ', fingerprint
    #image_data = cv2.imread("../test/11.jpg")
    cloudscreen = get_cloudscreen()
    image_data,time_stamp = cloudscreen.takeshot()
    #image_data = open('../test/11.jpg', 'rb').read()
    result, fingerprint = image_check.image_check(image_data)
    print result, fingerprint
    time.sleep(10)
    #image_data = cv2.imread("../test/12.jpg")
    image_data,time_stamp = cloudscreen.takeshot()
    result, fingerprint = image_check.image_check(image_data)
    print result, fingerprint