#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import unittest
from wetest.device import *

class CloudDeviceTester(unittest.TestCase):

    def setUp(self):
        """
            本地测试
        :return:
        """
        os.environ["PKGNAME"]="com.tencent.tmgp.NBAM"
        os.environ["LAUNCHACTIVITY"]="main"
        os.environ["ANDROID_SERIAL"]=AdbTool().device_serial()
        os.environ["PLAYFORM_PORT"]="5000"
        self.device = create_device()


    def test_get_rotation(self):
        rotation=self.device.get_rotation()
        print rotation


    def test_clear_app_data(self):
        self.device.clear_data("com.tencent.tmgp.NBAM")

    def tearDown(self):
        pass