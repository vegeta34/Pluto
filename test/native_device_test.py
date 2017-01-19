# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import unittest
from wetest.device import *


class NativeDeviceTester(unittest.TestCase):
    def setUp(self):
        """
            本地测试
        :return:
        """
        self.device = create_device()

    # def test_clear_data(self):
    #     self.device.clear_data("com.tencent.tmgp.NBAM")
    #     self.device.clear_data("com.tencent.mobileqq")
    #
    # def test_launch_app(self):
    #     self.device.launch_app()

    # def test_touch(self):
    #     self.device.touch(1431, 826)


    def test_get_displaysize(self):
        width,height=self.device.get_displaysize()
        print "width = {0},height = {1}".format(width,height)


    def test_get_rotation(self):
        rotation=self.device.get_rotation()
        print rotation
