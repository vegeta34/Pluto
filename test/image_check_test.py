# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'

import unittest
from imagetools.image_check import *
from cloudscreen.CloudScreen import *


class ImageCheckTester(unittest.TestCase):
    def setUp(self):
        self.image_check = ImageCheck()
        self.cloudscreen = get_cloudscreen()

    def test_image_check(self):
        image1 = self.cloudscreen.takeshot()
        time.sleep(5)
        image2 = self.cloudscreen.takeshot()
        result, fingerprint = self.image_check.image_check(image1)
        print result, 'fingerprint : ', fingerprint
        result, fingerprint = self.image_check.image_check(image2)
        print result, 'fingerprint : ', fingerprint

