#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from libs.uiauto.uiautomator import AutomatorDevice
from common.adb_process import *
from common.logger_config import *
import common.platform_helper as platform
import logging

logger=logging.getLogger(__name__)

_device_port=9008
_uiautomator_port = 19008
THIRD_MONKEY = True

def _init_uiautomator():
    """
        初始化uiautomator
    :return:
    """
    file_path = os.path.split(os.path.realpath(__file__))[0]
    uiautomator_stub_path = os.path.abspath(
        os.path.join(file_path,"..","libs","uiAutomator","uiautomator_stand_stub.jar"))
    #adb=AdbTool()
    excute_adb("push {0} /data/local/tmp".format(uiautomator_stub_path))

    logger.debug("Start UIAutomator")

    os.system("adb shell ps")
    call_adb_shell("adb forward tcp:{0} tcp:{1} && adb shell uiautomator runtest uiautomator_stand_stub.jar -c com.github.uiautomatorstub.Stub".format(_uiautomator_port,_device_port))
    # call_adb_shell(["shell","uiautomator","runtest","/data/local/tmp/uiautomator_stand_stub.jar","-c","com.github.uiautomatorstub.Stub","--nohup"])#--nohup

    time.sleep(5)
    forward(_uiautomator_port, _device_port)
    os.system("adb forward --list")
    os.system("adb shell ps")
    logger.debug("Exit uiautomator")


def _init():
    port = os.environ.get("UIAUTOMATORPORT")
    if port and not THIRD_MONKEY:#
        return int(port)
    else:
        """
            本地，初始化UiAutomator
        """
        _init_uiautomator()
        return int(_uiautomator_port)


def get_uiautomator():
    if get_uiautomator.instance:
        return get_uiautomator.instance
    else:
        port=_init()
        get_uiautomator.instance = AutomatorDevice(None, port, "localhost", None)
        return get_uiautomator.instance

get_uiautomator.instance=None


if __name__ == '__main__':
    _init_uiautomator()