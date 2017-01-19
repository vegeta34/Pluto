# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'

import unittest

from imagetools.image_upload import *
from cloudscreen.CloudScreen import *

class ImageUploadTester(unittest.TestCase):
    def setUp(self):
        self.image_upload = ImageUpload(203819, 11650)
        self.image_upload.set_image_index(20000)
        self.cloudscreen = get_cloudscreen()

    def test_image_upload(self):
        data = self.cloudscreen.takeshot()
        os.environ["PLATFORM_IP"] = "0.0.0.0"
        self.image_upload.data_save(data, "test.jpg")
        for i in range(0, 100):
            data = self.cloudscreen.takeshot()
            self.image_upload.upload_image(data, (50, 50), Color.PURPLE, 2)
            self.image_upload.upload_image(data, (50, 50), Color.PURPLE, 1)
            self.image_upload.upload_image(data, (50, 50), Color.PURPLE, 10)

