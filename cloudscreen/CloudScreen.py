# -*- coding: UTF-8 -*-

import struct
import traceback

from imagetools.image_upload import *
from common.adb_process import *
from SocketClient import SocketClient
from common.logger_config import *


logger = get_logger()

SNAP_SHOT_MODE = '\001'
MAX_TRIES = 3
FORWARD_PORT = 40004
PHONE_PORT = 25666
PUSH_SCREENCAPTURE = "push ./cloudscreen /data/local/tmp/cloudscreen/cloudscreen"
PUSH_SCREENCAPTURE_SO = "push ./libs/android-{0}/armeabi-v7a/cloudscreen.so /data/local/tmp/cloudscreen/cloudscreen"
CHMOD_SCREENCAPTURE = "shell chmod 777 /data/local/tmp/cloudscreen/cloudscreen"
LAUNCH_SCREENCAPTURE = "shell LD_LIBRARY_PATH=/data/local/tmp/cloudscreen /data/local/tmp/cloudscreen/cloudscreen -w {0} -h {1}"
LAUNCH_SCREENCAPTURE2 = "shell LD_LIBRARY_PATH=/data/local/tmp/cloudscreen /data/local/tmp/cloudscreen/cloudscreen -s -w {0} -h {1}"
DEL_SCREENCAPTURE = "rm /data/local/tmp/cloudscreen"
FORWARD = "forward tcp:{0} tcp:{1}".format(FORWARD_PORT, PHONE_PORT)
REMOVE_FORWARD = "forward --remove tcp:{0}".format(FORWARD_PORT)


class CloudCommand(object):
    CMD_SCREENCAP = '\003'


class CloudPacket(object):
    def __init__(self, command=CloudCommand.CMD_SCREENCAP, type=SNAP_SHOT_MODE, params=0):
        self.command = command
        self.type = type
        self.params = params

    def pack(self):
        return struct.pack("<2c2xi", self.command, self.type, self.params)


class CloudScreen(object):
    def __init__(self, width=360, height=640):
        port = os.environ.get("IMAGE_ENCODER_PORT")
        self.screen_address = os.environ.get("PLATFORM_IP", "127.0.0.1")
        if port:
            global FORWARD_PORT
            FORWARD_PORT = int(port)
        else:
            excute_adb(PUSH_SCREENCAPTURE)
            excute_adb(PUSH_SCREENCAPTURE_SO.format(self._get_version()))
            excute_adb(CHMOD_SCREENCAPTURE)
            self.sub_process = excute_adb_process_daemon(LAUNCH_SCREENCAPTURE.format(width, height))
            excute_adb(FORWARD)
        self.testid = os.getenv("TESTID","1234")
        self.deviceid = os.getenv("DEVICEID", "1234")
        self.image_uploader = ImageUpload(self.testid, self.deviceid)
        self.image_check = get_image_check()

    def _get_version(self):
        file = excute_adb("shell getprop ro.build.version.sdk")
        version = file.read()
        file.close()
        version = version.replace("\r\n", "")
        version = version.replace("\n", "")
        logger.info("get_version: {0}".format(version))
        if version not in ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "N"]:
            logger.warn("not supported version")
            return ""
        return version

    def takeshot(self):
        socket_client = None
        try:
            logger.info("get raw data from cloudscreen")
            socket_client = SocketClient(self.screen_address, FORWARD_PORT)
            cloud_packet = CloudPacket(CloudCommand.CMD_SCREENCAP, SNAP_SHOT_MODE, 0)
            buffer = cloud_packet.pack()
            socket_client.send(buffer)
            head = socket_client.recv(16)  # int seq; int length; int64 timestamp;
            seq, length, timestamp, drop = struct.unpack("<2i2i", head)
            logger.info("image length: {0} timestamp: {1}".format(length, timestamp))
            image_data = socket_client.recv(length)
            socket_client.close()
            timestamp *= 1000
            return image_data, timestamp
        except:
            logger.error("takeshot failed...")
            traceback.print_exc()
            try:
                if socket_client:
                    socket_client.close()
            except:
                logger.error("Error: Close socket error!")
        logger.error("Error: Can not take shot now!")

    def stop(self):
        port = os.environ.get("IMAGEPORT")
        if not port and self.sub_process:
            self.sub_process.kill()
            excute_adb(REMOVE_FORWARD)

    def screenshot(self,point=None,tag_color=Color.RED,radius=8):
        logger.info("screenshot point: {0}".format(point))
        image_data, timestamp = self.takeshot()
        result, fingerprint = self.image_check.image_check(image_data)
        self.image_uploader.upload_image(image_data,point,result,tag_color,radius,timestamp)
        return image_data

    def upload_image(self,image,point=None,issame=False,tag_color=Color.RED,radius=8,timestamp=time.time() * 1000):
        try:
            index=self.image_uploader.upload_image(image, point,issame, tag_color, radius, timestamp)
            return index
        except:
            logger.error("upload image error")

        return -1


def get_cloudscreen(width=360, height=640):
    if get_cloudscreen.instance:
        return get_cloudscreen.instance
    get_cloudscreen.instance = CloudScreen(width, height)
    return get_cloudscreen.instance


get_cloudscreen.instance = None

if __name__ == "__main__":
    cloudscreen = get_cloudscreen()
    time.sleep(5)
    data,timestamp = cloudscreen.takeshot()
    # timestamp = struct.unpack("<2i", struct.pack("<q", timestamp))[0]
    print time.time(), timestamp
    time.sleep(5)
    print len(data)
    f = open("test.jpg", 'wb')
    f.write(data)
    f.flush()
    f.close()
    time.sleep(20)
    cloudscreen.stop()
