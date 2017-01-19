#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import time, logging, re, traceback
import uiautomator_manager as m
import login_getter as getter

logger = logging.getLogger("wetest")

uiauto = m.get_uiautomator()


def __click_by_step__(obj, step, number):
    if obj.exists:
        info = obj.info
        local_x = (info['bounds']['left'] + info['bounds']['right']) / 2
        local_y = info['bounds']['bottom']
        for y in range(local_y, local_y + step * number, step):
            uiauto.click(local_x, y)
        return


def _login_edit_box(account, pwd):
    logins = getter.get_login()
    if logins:
        try:
            local_step = 10
            local_range = 20
            local_x = uiauto.info['displayWidth']
            user_edit = logins[0]
            info = user_edit.info
            local_y = (info['bounds']['top'] + info['bounds']['bottom']) / 2
            while None == re.search(account, user_edit.get_text(), re.IGNORECASE):
                # click the x point
                for i in range(0, local_range):
                    uiauto.click(local_x - i * local_step, local_y)
                    logger.info(
                        "click the usr x point. local_x is " + str(local_x - i * local_step) + ". local_y is " + str(
                            local_y))
                uiauto.wait.idle()
                user_edit.set_text(account)
                uiauto.wait.update()
                # user
                logger.info("src and dest content.")
                logger.info(user_edit.get_text())
                logger.info(account)
            # pwd
            pwd_edit = logins[1]
            info = pwd_edit.info
            local_y = (info['bounds']['top'] + info['bounds']['bottom']) / 2
            for j in range(0, local_range):
                uiauto.click(local_x - j * local_step, local_y)
                logger.info(
                    "click the pwd x point. local_x is " + str(local_x - j * local_step) + ". local_y is " + str(
                        local_y))
            uiauto.wait.idle()
            pwd_edit.set_text(pwd)
            logger.info("set pwd : " + pwd)
            # login
            uiauto.wait.idle()
            login_button = logins[2]
            login_button.click.wait()
            logger.info("login_button.click()")
            return True
        except Exception, e:
            logger.info(e)
            stack = traceback.format_exc()
            logger.error(stack)
    return False


def _login_qq():
    # qq
    try:
        if uiauto(text=u'登录失败', className=u'android.widget.TextView').exists and uiauto(text=u'确定',
                                                                                        className=u'android.widget.TextView').exists:
            btn = uiauto(text=u'确定', className=u'android.widget.TextView')
            if uiauto(text=u'请输入帐号(错误码: 3103)', className=u'android.widget.TextView').exists:
                __click_by_step__(btn, 20, 15)
                pass
            elif uiauto(text=u'请输入密码(错误码: 3104)', className=u'android.widget.TextView').exists:
                __click_by_step__(btn, 20, 15)
            else:
                uiauto.wait.idle()
                btn.click()
            logger.info("this. 登录失败")

        elif uiauto(text=u'QQ登录').exists \
                and uiauto(text=u'重新拉取授权信息', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'重新拉取授权信息', className=u'android.widget.Button').click()
            logger.info("this.QQ登录")

        elif uiauto(text=u'QQ登录').exists \
                and uiauto(text=u'授权并登录', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'授权并登录', className=u'android.widget.Button').click()
            logger.info("this. 授权并登录")

        elif uiauto(text=u'QQ登录').exists \
                and uiauto(text=u'登录', className='android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'登录', className='android.widget.Button').click()
            logger.info("this. QQ登录")

        elif uiauto(text=u'输入验证码').exists \
                and uiauto(className=u'android.widget.EditText').exists \
                and uiauto(text=u'取消').exists:
            uiauto.wait.idle()
            uiauto(text=u'取消').click()
            logger.info("this. 输入验证码")

    except Exception, e:
        logger.info(e)


def _login_wx():
    try:
        if uiauto(className=u'com.tencent.smtt.webkit.WebView').exists or uiauto(className=u'android.webkit.WebView').exists \
                or uiauto(className=u'android.view.View'):
            height = uiauto.info["displayHeight"]
            width = uiauto.info["displayWidth"]
            x = width / 2
            if uiauto(text=u'微信登录').exists:
                for y in range(height * 4 / 5, height * 1 / 5, -1 * height / 50):
                    uiauto.wait.idle()
                    uiauto.click(x, y)
                    logger.info(str(x) + ", " + str(y))
        elif uiauto(text=u'微信登录', className=u'android.widget.TextView').exists \
                and 1 == uiauto(className=u'android.widget.Button').count \
                and 1 == uiauto(className=u'android.widget.Image').count \
                and 0 == uiauto(className=u'android.widget.EditText').count:
            uiauto.wait.idle()
            uiauto(className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'帐号或密码错误，请重新填写。', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'抱歉，出错了', className=u'android.widget.TextView').exists \
                and uiauto(className=u'com.tencent.smtt.webkit.WebView').exists \
                and uiauto(description=u'返回').exists:
            uiauto.wait.idle()
            uiauto(description=u'返回').click()
            logger.info("this.")

        elif uiauto(text=u'该用户不存在', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'你操作频率过快，请稍后重试', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(text=u'填写验证码', className=u'android.widget.TextView').exists \
                and uiauto(text=u'继续', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto.press.back()
            logger.info("this.")

        elif uiauto(textStartsWith=u'当前帐号的使用存在异常', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(textStartsWith=u'你登录的微信需要进行好友验证', className=u'android.widget.TextView').exists \
                and uiauto(text=u'取消', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'取消', className=u'android.widget.Button').click()
            logger.info("this.")

        elif uiauto(textStartsWith=u'微信帐号不能为空', className=u'android.widget.TextView').exists \
                and uiauto(text=u'确定', className=u'android.widget.Button').exists:
            uiauto.wait.idle()
            uiauto(text=u'确定', className=u'android.widget.Button').click()
            logger.info("this.")

    except Exception, e:
        logger.info(e)


def login_tencent(account, pwd, timeout=60):
    start_time = time.time()
    end_time = start_time

    while end_time - start_time < timeout:
        _login_edit_box(account, pwd)
        package_name = uiauto.info["currentPackageName"]
        if package_name == "com.tencent.mobileqq":
            _login_qq()
        elif package_name == "com.tencent.mm":
            _login_wx()
        else:
            return True
        end_time = time.time()
    return False

# login_tencent("2952020383", "wetesth")
