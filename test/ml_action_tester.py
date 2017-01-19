#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import unittest
from wetest.ml_client import *

class MlClientTester(unittest.TestCase):

    # def test_get_actions(self):
    #     ml=MlClient(12085,12111,"com.tencent.wetest.demo","2.1.0")
    #     res=ml.get_action(128718,4)
    #     print res


    # def test_report_action(self):
    #     ml=MlClient(12085,12111,"com.tencent.wetest.demo","2.1.0")
    #     res=ml.report_action(128718,121111,{"x": 1111, "y": 2222, "width": 1280, "height": 720, "interval": 3, "type": 0, "source": 0},True)
    #     print res
    #     res=ml.get_action(128718,4)

    # def test_start_session(self):
    #     ml=MlClient(12085,12111,"com.tencent.wetest.demo","2.1.0")
    #     ml.start_session(1280,720)
        # res=ml.get_action(128718,4)
        # print res
        # print res["actions"]

    def _full_test(self):
        ml=MlClient(12085,12111,"com.tencent.wetest.client","2.1.0")
        # ml.start_session(1280,720)
        #
        # first_find = ml.get_action(121112, 1280, 720)
        # print(first_find)
        # pre = {
        #     "fingerprint": 121112,
        #     "seq": 0
        # }
        #
        # current = {
        #     "fingerprint": 121111,
        #     "seq": 1
        # }
        # report_action=first_find["actions"][0]
        # print("report action {0}".format(report_action))
        # ml.report_action(pre, current,report_action , True)
        #
        # second_find = ml.get_action(121112, 1280, 720)
        # print("next find action")
        # print(second_find)
        ml.close_session()

    def test_all(self):
        for i in range(1):
            self._full_test()

