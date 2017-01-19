# -*- coding: UTF-8 -*-
__author__ = 'alexkan'

import unittest
from cloudscreen.CloudScreen import *
import numpy as np
import cv2

class CloudScreenTester(unittest.TestCase):
    def setUp(self):
        """
            本地测试
        :return:
        """
        self.cloudscreen = get_cloudscreen()

    def test_takeshot(self):
        data = self.cloudscreen.takeshot()
        # print len(data)
        # f = open("test.jpg", 'wb')
        # f.write(data)
        # f.flush()
        # f.close()
        data = np.frombuffer(data, dtype=np.uint8)
        img=cv2.imdecode(data,0)
        cv2.imshow("img",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("recv2.jpg",img)
        self.cloudscreen.stop()

