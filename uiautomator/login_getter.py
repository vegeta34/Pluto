# -*- coding: UTF-8 -*-

import traceback
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import uiautomator_manager as m

uiauto = m.get_uiautomator()


def is_login(pkg=""):
    xml = uiauto.dump(compressed=False)
    root = ET.fromstring(xml.encode('utf-8'))

    # 有些界面只有密码框，不是登录，例如微信支付。
    edits = root.findall(".//node[@class='android.widget.EditText']")
    if len(edits) < 2:
        return False

    elements = root.findall(".//node[@class='android.widget.EditText'][@password='true']")
    if len(elements) > 0:
        return True

    # 三星等一部分手机特殊处理
    elements = root.findall(".//node[@class='android.widget.EditText']")
    new_elements = []
    for element in elements:
        text = element.get("text")
        if u"密码" in text:
            new_elements.append(element)
    elements = new_elements
    if len(elements) > 0:
        return True
    # 平台上每次会清理微信QQ帐号，并不会存在微信或者QQ已经登录进行授权的场景，故注释下面三行。
    # current_pkg = uiauto.info["currentPackageName"]
    # if (current_pkg=="com.tencent.mobileqq" or current_pkg=="com.tencent.mm") and pkg!="com.tencent.mobileqq" and pkg!="com.tencent.mm":
    #     return True
    return False

def test_dump():
    xml = uiauto.dump(compressed=False)
    root = ET.fromstring(xml.encode('utf-8'))
    elements = root.findall(".//node[@clickable='true']")
    print xml
    print elements[0]

# 判断当前界面是否是登录界面，如果是返回，如果不是返回[]
def get_login():
    xml = uiauto.dump(compressed=False)
    root = ET.fromstring(xml.encode('utf-8'))
    user_pass = []
    elements = root.findall(".//node[@class='android.widget.EditText'][@password='true']")
    if len(elements)==1:
        pass_edit = elements[0]
        resourceid = pass_edit.get("resource-id", "")
        password = None
        if len(resourceid)>0:
            pass_uiauto = uiauto(className=u'android.widget.EditText', resourceId=resourceid)
        else:
            pass_uiauto = uiauto(className=u'android.widget.EditText')
        if pass_uiauto.count==1:
            password = pass_uiauto
        else:
            for view in pass_uiauto:
                left = view.info[u'bounds'][u'left']
                top = view.info[u'bounds'][u'top']
                right = view.info[u'bounds'][u'right']
                bottom = view.info[u'bounds'][u'bottom']
                bounds = '[{0},{1}][{2},{3}]'.format(left, top, right, bottom)
                if bounds==pass_edit.get("bounds",""):
                    password = view
                    break
        if password == None or not password.exists:
            return user_pass
        user_uiauto = password.up(className=u'android.widget.EditText')
        if user_uiauto == None or not user_uiauto.exists:
            user_uiauto = password.left(className=u'android.widget.EditText')
        if user_uiauto == None or not user_uiauto.exists:
            user_uiauto = uiauto(className=u'android.widget.EditText')
        if user_uiauto == None or not user_uiauto.exists:
            return user_pass
        login_uiauto = password.down(className=u'android.widget.Button', textContains=u'登')
        if login_uiauto == None or not login_uiauto.exists:
            login_uiauto = password.right(className=u'android.widget.Button', textContains=u'登')
        if login_uiauto == None or not login_uiauto.exists:
            login_uiauto = uiauto(className=u'android.widget.Button', textContains=u'登')
        if login_uiauto == None or not login_uiauto.exists:
            login_uiauto = password.down(className=u'android.widget.Button')
        if login_uiauto == None or not login_uiauto.exists:
            login_uiauto = password.right(className=u'android.widget.Button')
        if login_uiauto == None or not login_uiauto.exists:
            login_uiauto = uiauto(className=u'android.widget.Button')
        if login_uiauto == None or not login_uiauto.exists:
            return user_pass
        user_pass.append(user_uiauto)
        user_pass.append(password)
        user_pass.append(login_uiauto)
    return user_pass
#test_dump()
