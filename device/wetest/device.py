# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from functools import wraps

import uiautomator.uiautomator_manager as ui_manager
from httptools.remote_connection import Method
from httptools.exceptions import *
import uiautomator.login_tencent as login
import common.platform_helper as platform
import local_config as config
from cloudscreen.CloudScreen import *

logger = logger_config.get_logger()


def exception_call_super(fn):
    """
        很多方法请求平台时，有可能出现问题。请求平台出现问题时，可以直接尝试使用本地方法。
        CloudDevice调用失败时，直接调用Device里面相同名称的方法
    :param fn:
    :return:
    """

    @wraps(fn)
    def wrap_function(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (WeTestRuntimeError, ConnectionException):
            logger.warn("call cloud function {0} error".format(fn.__name__))
            return getattr(super(CloudDevice, args[0]), fn.__name__)(*args[1:], **kwargs)

    return wrap_function


class Device(object):
    """
        与设备操作相关的内容
    """

    def __init__(self, serial, package, activity, uiautomator):
        self.serial = serial
        self.package = package
        self.activity = activity
        self._adb = AdbTool(os.environ.get("ANDROID_SERIAL", None), os.environ.get("PLATFORM_IP", "127.0.0.1"))
        self.uiautomator = uiautomator
        self.has_login = False
        self._display_width, self._display_height = self.get_displaysize()
        self._refresh = 0
        self.rotation = 0
        width, height = self._display_width, self._display_height
        if width > height:
            width, height = height, width
        target_width = 640 * width / height
        self.cloudscreen = get_cloudscreen(target_width, 640)
        self.default_test_time = 300

    @property
    def adb(self):
        return self._adb

    @property
    def uiauto(self):
        return self.uiautomator

    def clear_data(self, package=None):
        """
            清除数据
        :return:
        """
        logger.info("device clear data: {0}".format(package))
        if not package:
            self.adb.cmd_wait("shell", "pm", "clear", self.package)
            return
        self.adb.cmd_wait("shell", "pm", "clear", package)

    def launch_app(self, package=None, activity=None):
        """
            拉起游戏，可以返回pid和拉起时间
        :return:
        """
        pass

    def touch(self, x, y):
        """
            屏幕点击操作
        :param x:左上角为0
        :param y:左上角为0
        :return:
        """
        logger.info("click x: {0} y: {1}".format(x, y))
        self.touchcapture(x, y)
        self.uiauto.click(x, y)


    def swipe(self, sx, sy, ex, ey):
        """
        滑动操作
        :param sx:
        :param sy:
        :param ex:
        :param ey:
        :return:
        """
        self.uiauto.swipe(sx, sy, ex, ey)

    def long_click(self, x, y):
        """
        长按
        :param x:
        :param y:
        :return:
        """
        self.uiauto.long_click(x, y)

    def click(self, x, y):
        """
        长按
        :param x:
        :param y:
        :return:
        """
        self.uiauto.click(x, y)

    def screenshot(self):
        """
            屏幕截图
        :return:
        """
        logger.debug("device screenshot")
        self.cloudscreen.screenshot()

    def _refresh_display(self):
        try:
            self._display_width, self._display_height = self.get_displaysize()
            self.rotation = self.get_rotation()
            self._refresh = 1
        except:
            stack = traceback.format_exc()
            logger.error(stack)

    @property
    def display_width(self):
        if self._refresh % 20 == 0:
            self._refresh_display()
        self._refresh += 1
        return self._display_width

    @property
    def display_height(self):
        if self._refresh % 20 == 0:
            self._refresh_display()
        self._refresh += 1
        return self._display_height

    def unified(self, target_x, target_y):
        """
        返回高为640的点击位置
        :return:
        """
        logger.info("unify")
        image_height = 640.0
        width, height = self.display_width, self.display_height
        if width > height:
            image_width = image_height * height / width
        else:
            image_width = image_height * width / height

        if self.rotation == 0:
            x = target_x
            y = target_y
        elif self.rotation == 1:
            x = height - target_y
            y = target_x
        elif self.rotation == 2:
            x = width - target_x
            y = height - target_y
        else:
            x = target_y
            y = width - target_x
        x *= (image_width / min(width, height))
        y *= (image_height / max(width, height))
        logger.info("after unify: {0}, {1}".format(int(x), int(y)))
        return int(x), int(y)

    def touchcapture(self, x, y):
        logger.info("touchcapture: ({0},{1})".format(x, y))
        self.cloudscreen.screenshot(self.unified(x, y))

    def forward(self, remote_port):
        """
            forward
        :return:
        """
        logger.debug("native umimplement forward")

    def get_displaysize(self):
        """
            获取屏幕长宽高
        :return: width,height,单位为pix
        """
        try:
            width = self.uiauto.info["displayWidth"]
            height = self.uiauto.info["displayHeight"]
        except:
            logger.error("get device error: {0}".format(traceback.format_exc()))
            width = 1080
            height = 1920
        return width, height

    def get_rotation(self):
        """
            获取屏幕转向
        :return:返回0,1,2,3
        left/l:       rotation=90 , displayRotation=1
        right/r:      rotation=270, displayRotation=3
        natural/n:    rotation=0  , displayRotation=0
        upsidedown/u: rotation=180, displayRotation=2
        """
        return self.uiauto.info["displayRotation"]

    def get_current_package(self):
        """
        
        :return:
        """
        logger.info("uiauto get current package")
        return self.uiauto.info["currentPackageName"]

    def force_app_front(self):
        """
        保证测试的APP在前面
        :return:
        """
        current_pkg = self.get_current_package()
        if current_pkg != self.package and current_pkg != "com.tencent.mobileqq" and current_pkg != "com.tencent.mm":
            logger.info("FORCE APP FRONT")
            self.launch_app(self.package, self.activity)

    def get_test_time(self):
        """
        获取测试的时间
        :return:
        """
        return self.default_test_time

    def stop_platform_uiautomator(self):
        pass

    def start_platform_uiautomator(self):
        pass

    def kill_app(self):
        logger.info("now kill app")
        self.adb.cmd("shell am force-stop " + self.package)
        self.screenshot()
        time.sleep(2)
        self.screenshot()

    def login_tencent(self):
        """
            QQ和微信的登陆
        :return:
        """
        _current_pkgname = self.get_current_package()
        account = os.environ.get("OTHERNAME")
        pwd = os.environ.get("OTHERPWD")
        if _current_pkgname == "com.tencent.mobileqq":
            if not account or not pwd:
                account = os.environ.get("QQNAME")
                pwd = os.environ.get("QQPWD")
            if not account or not pwd:
                account = "1619798946"
                pwd = "wetestv"
        elif _current_pkgname == "com.tencent.mm":
            if not account or not pwd:
                account = os.environ.get("WECHATNAME")
                pwd = os.environ.get("WECHATPWD")
            if not account or not pwd:
                account = "rdgztest_60061"
                pwd = "wetestd"
        else:
            if not account or not pwd:
                account = "1619798946"
                pwd = "wetestv"
        self.has_login = login.login_tencent(account, pwd)


class NativeDevice(Device):
    def __init__(self, serial, package, activity, uiautomator):
        super(NativeDevice, self).__init__(serial, package, activity, uiautomator)

    def launch_app(self, package=None, activity=None):
        """
            拉起游戏，可以返回pid和拉起时间
        :return:
        """
        if package == None or activity == None:
            package = self.package
            activity = self.activity

        content = self.adb.cmd_wait("shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1")
        logger.debug(content)
        return 0, 0


class Command(object):
    GET_ROTATION = (Method.GET, "rotation")
    CLEAR_APP_DATA = (Method.POST, "clearappdata")
    LAUNCH_APP = (Method.POST, "launchapp")
    TOUCH_CAPTURE = (Method.POST, "touchcapture")
    CURRENT_PACKAGE_NAME = (Method.GET, "currentpackagename")
    RESOLUTION = (Method.GET, "resolution")
    CAPTURE = (Method.POST, "snapshot")
    STOP_UIAUTOMATOR = (Method.POST, "pauseuiautomator")
    START_UIAUTOMATOR = (Method.POST, "resumeuiautomator")
    TOUCH = (Method.POST, "touch")
    GET_TEST_TIME = (Method.GET, "runtime")
    FORWARD = (Method.POST, "forward")


class CloudDevice(Device):
    def __init__(self, serial, package, activity, uiautomator, hostip, port):
        super(CloudDevice, self).__init__(serial, package, activity, uiautomator)
        self.port = port
        self._touch_capture_sequence = 0
        self.width = 0
        self.height = 0
        self.platform_helper = platform.get_platform_client()

    def forward(self, remote_port):
        response = self.platform_helper.platform_forward(remote_port)
        if response:
            return response["localPort"]

    # @exception_call_super
    def launch_app(self, package=None, activity=None):
        if package == None or activity == None:
            package = self.package
            activity = self.activity
        response = self.platform_helper.launch_app(package, activity)
        if response:
            return response

    # @exception_call_super
    # def screenshot(self):
    #     self._touch_capture_sequence += 1
    #     response = self.platform_helper.take_screenshot()
    #     if response:
    #         return response



    def start_platform_uiautomator(self):
        response = self.platform_helper.resume_uiautomator()
        return response

    def stop_platform_uiautomator(self):
        response = self.platform_helper.pause_uiautomator()
        return response

    @exception_call_super
    def get_test_time(self):
        response = self.platform_helper.get_runtime()
        return response['runtime']

    def force_app_front(self):
        """
        保证测试的APP在前面
        :return:
        """
        logger.info("check app front")
        current_pkg = self.get_current_package()
        logger.info("now package name is {0}".format(current_pkg))
        if current_pkg != self.package and current_pkg != "com.tencent.mobileqq" and current_pkg != "com.tencent.mm":
            # 判断是否有允许按钮
            try:
                allow_button = self.uiauto(className="android.widget.Button", text=u'允许')
                if allow_button and allow_button.exists:
                    allow_button.click()
                    return
            except:
                return
            logger.info("FORCE APP FRONT")
            self.kill_app()
            logger.info("relaunch app")
            self.launch_app(self.package, self.activity)


def create_device():
    pkgname = os.environ.get("PKGNAME", "com.tencent.tmgp.sgame")
    activity_name = os.environ.get("LAUNCHACTIVITY")
    serial = os.environ.get("ANDROID_SERIAL")
    hostip = os.environ.get("PLATFORM_IP", "127.0.0.1")
    uiauto = ui_manager.get_uiautomator()
    platform_port = os.environ.get("PLATFORM_PORT")
    if platform_port:
        return CloudDevice(serial, pkgname, activity_name, uiauto, hostip, platform_port)
    else:
        # 本地运行
        # 云端运行
        pkgname = config.PACKAGENAME
        activity_name = ""
        serial = ""
        return NativeDevice(serial, pkgname, activity_name, uiauto)


def get_device():
    if not get_device.instance:
        get_device.instance = create_device()
    return get_device.instance


get_device.instance = None
