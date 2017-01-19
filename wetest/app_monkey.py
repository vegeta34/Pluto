# -*- coding: UTF-8 -*-
__author__ = 'alexkan'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import logging, re, traceback, random

logger = logging.getLogger(__name__)

APP_THRESHOLD = 10

class ElementWraper(object):
    """
    该类存在的意义就是保存uiauto selector 返回的element的info,避免重复请求（每次element.info实际会有一次请求）。
    """
    def __init__(self, element):
        self.element = element
        self.info = element.info

class APPMonkey(object):

    def __init__(self, device):
        self.device = device
        self.uiauto = device.uiauto
        self.cloudscreen = device.cloudscreen
        self.first_round = True
        self.has_visited = []
        self.is_xml = True
        self.is_app = False
        self._display_width, self._display_height = 1080, 1920
        self._refresh = 0
        self.rotation = 0
        self.none_count = 0

    def _refresh_display(self):
        try:
            self._display_width, self._display_height = self.device.get_displaysize()
            self.rotation = self.device.get_rotation()
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

    def unique_string(self, element):
        if ET.iselement(element):
            return "{0}|{1}|{2}|{3}".format(element.get("class", ""),element.get("resource-id", ""),element.get("index", ""),element.get("bounds", ""))
        else:
            info = element.info
            return "{0}|{1}|{2}".format(info["className"],info["contentDescription"],info["bounds"])

    def get_element_info(self, element):
        if ET.iselement(element):
            info = {}
            info["contentDescription"] = element.get("class", "")
            info["scrollable"] = element.get("scrollable", "") == "true"
            info["checked"] = element.get("checked","") == "true"
            info["bounds"] = self._get_bound(element)
            info["className"] = element.get("class","")
            info["longClickable"] = element.get("long-clickable","") == "true"
            return info
        else:
            return element.info

    def _get_bound(self, element):
        if ET.iselement(element):
            bound_str = element.get("bounds", "")
            if len(bound_str) <= 0:
                return None
            regex = "\[(\d+),(\d+)\]\[(\d+),(\d+)\]"
            match = re.search(regex, bound_str)
            bound = {}
            if match:
                bound["left"] = int(match.group(1))
                bound["top"] = int(match.group(2))
                bound["right"] = int(match.group(3))
                bound["bottom"] = int(match.group(4))
            return bound
        else:
            return element.info["bounds"]

    def set_text(self, element, text):
        logger.info("uiauto set edit text: {0}".format(text))
        if ET.iselement(element):
            elements = self.uiauto(className="android.widget.EditText")
            if not elements or elements.count == 0:
                return False
            for edit in elements:
                info = edit.info
                left = info[u'bounds'][u'left']
                top = info[u'bounds'][u'top']
                right = info[u'bounds'][u'right']
                bottom = info[u'bounds'][u'bottom']
                bounds = '[{0},{1}][{2},{3}]'.format(left, top, right, bottom)
                if bounds == element.get("bounds", ""):
                    logger.info("uiauto set text")
                    edit.set_text(text)
                    return True
        else:
            element.element.set_text(text)
        return True

    def long_click(self, x, y):
        logger.info("uiauto long click")
        self.cloudscreen.screenshot(self.unified(x, y))
        self.uiauto.long_click(x, y)

    def swipe(self, sx, sy, ex, ey):
        logger.info("uiauto swipe")
        self.cloudscreen.screenshot()
        self.uiauto.swipe(sx, sy, ex, ey)


    def get_clickable(self):
        try:
            self.is_xml = True
            xml = self.uiauto.dump(compressed=False)
            root = ET.fromstring(xml.encode('utf-8'))
            elements = root.findall(".//node[@clickable='true']")
            viewpages = root.findall(".//node[@class='android.support.v4.view.ViewPager']")
            elements.extend(viewpages)
        except:
            """
            讨厌的很，在一些版本的Android系统上不支持富文本显示，dump会报错，简直是日了狗，带来一些麻烦，不能统一处理。
            """
            self.is_xml = False
            elements = self.uiauto(clickable=True)
            viewpages = self.uiauto(className="android.support.v4.view.ViewPager")
            elements.extend(viewpages)
        return elements

    def pick_element(self,elements):
        logger.info("there are {0} clickable elements".format(len(elements)))
        try:
            if self.is_xml:
                unvisited = []
                for element in elements:
                    str = self.unique_string(element)
                    if str not in self.has_visited:
                        unvisited.append(element)
                logger.info("there are {0} unvisited elements".format(len(unvisited)))
                if len(unvisited)>0:
                    return random.choice(unvisited)
                r = random.randint(0, len(elements))
                if r == len(elements):
                    return None
                else:
                    return elements[r]
            else:
                if len(elements) > 0:
                    return random.choice(elements)
                else:
                    return None
        except:
            stack = traceback.format_exc()
            logger.error(stack)

    def visit(self, element):
        try:
            logger.info("visit {0}".format(element))
            bounds = self._get_bound(element)
            info = self.get_element_info(element)
            center_x = (bounds["left"] + bounds["right"]) / 2
            center_y = (bounds["top"] + bounds["bottom"]) / 2
            if info["className"] == "android.support.v4.view.ViewPager":
                logger.info("ViewPager")
                view_width = bounds["right"] - bounds["left"]
                view_height = bounds["bottom"] - bounds["top"]
                width = self.display_width
                height = self.display_height
                if view_width >= 0.8*width and view_height >= 0.8*height:
                    self.welcome_page()
                else:
                    self.cloudscreen.screenshot()
                    up = random.randint(0, 2)
                    if up != 0:
                        self.swipe(bounds["right"],center_y,bounds["left"],center_y)
                    else:
                        self.swipe(center_x, bounds["bottom"], center_x, bounds["top"])

            elif info["scrollable"]:
                #滑动
                logger.info("just swipe")
                self.cloudscreen.screenshot()
                up = random.randint(0, 2)
                if up == 0:
                    self.swipe(center_x, center_y, center_x, bounds["top"])
                else:
                    self.swipe(center_x, center_y, center_x, bounds["bottom"])
            elif info["className"] == "android.widget.EditText":
                #输入
                logger.info("EditText input")
                random_str = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789', 6))
                logger.info("set text {0}".format(random_str))
                self.set_text(element, random_str)
            elif info["longClickable"]:
                #长按
                logger.info("long click")
                self.long_click(center_x, center_y)
            else:
                #点击
                logger.info("click")
                self.cloudscreen.screenshot(self.unified(center_x, center_y))
                self.uiauto.click(center_x, center_y)
            self.has_visited.append(self.unique_string(element))
        except:
            stack = traceback.format_exc()
            logger.error(stack)


    def welcome_page(self):
        logger.info("now swipe 6 times")
        info = self.uiauto.info
        width = info["displayWidth"]
        height = info["displayHeight"]
        for i in range(0, 6):
            self.swipe(width - 30, height / 2, 30, height / 2)

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

    def _random_click(self):
        x1 = random.randint(0, self.display_width)
        y1 = random.randint(20, self.display_height)  # 避免oppo vivo手机点击到关闭USB选项黄条
        logger.info("random click: {0} {1}".format(x1, y1))
        self.cloudscreen.screenshot(self.unified(x1, y1))
        self.uiauto.click(x1, y1)

    def app_round(self):
        elements = self.get_clickable()
        if len(elements) > APP_THRESHOLD:
            if not self.is_app:
                currentpkg = self.device.get_current_package()
                if currentpkg == self.device.package:
                    logger.info("now set is_app is true")
                    self.is_app = True
        if self.first_round:
            self.first_round = False
            logger.info("first found {0} elements".format(len(elements)))
            if len(elements) == 0:
                return True
            # if len(elements) < 4:
            #     # 滑动
            #     self.welcome_page()
        element = self.pick_element(elements)
        logger.info("returned element: {0}".format(element))
        if element is None:
            self.none_count += 1
            # 如果确定是应用则点击返回或者随机选一个elements.
            if self.is_app:
                # press back
                logger.info("now press back")
                self.uiauto.press.back()
                self.is_app = False
                return False
            elif self.none_count <= 3:
                self._random_click()
                return False
            else:
                logger.info("now return and set is_game true")
                return True
        else:
            self.visit(element)
            return False



