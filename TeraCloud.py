#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import re
import os


class TeraCloud:
    def __init__(self, username, password, sleep_time=6, debug=False):
        # TODO: add timeout function
        """
        TeraCloud类初始化

        :param username: 用户名
        :param password: 密码
        :param sleep_time: 休眠时间，用于等待页面加载
        :param debug: Debug模式，True则显示浏览器，False则不显示
        """
        self.username = username
        self.password = password
        self.sleep = sleep_time
        self.browser_source = None

        driver_path = "ChromeDriver/chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        if not debug:  # 不显示浏览器
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        if not os.path.exists(driver_path):
            raise Exception("chromedriver.exe not found")
        chrome_service = Service(driver_path)
        self.browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
        # 规避检测
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """   
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
        })

    def get_browser_source(self):
        """
        调用获取信息前必须先调用此函数，获取File Browser页面源码

        :return: boolean, string
        """
        url_origin = "https://teracloud.jp/en/"
        url_browser1 = "https://uno.teracloud.jp/browser/"
        url_browser2 = "https://yura.teracloud.jp/browser/"
        try:
            print("Opening browser...")
            self.browser.get(url_origin)
            print("Opening login page...")
            self.browser.find_element(By.CLASS_NAME, 'header-navi-li-login').click()  # 进入登录页面
            self.browser.find_element(By.NAME, 'id').send_keys(self.username)
            self.browser.find_element(By.NAME, 'password').send_keys(self.password)
            print("Logging in...")
            self.browser.find_element(By.ID, 'loginbtn').click()  # 登录
            if self.browser.current_url == 'https://login.teracloud.jp/oauth2/auth':
                return False, "login failed"
            print("Login successfully")
        except Exception as e:
            return False, "Login failed\n" + str(e)

        # 进入File Browser页面
        print("Opening File Browser...")
        try:
            self.browser.get(url_browser1)
        except Exception:
            try:
                self.browser.get(url_browser2)
            except Exception as e:
                return False, "Get browser failed\n" + str(e)

        print("Waiting for page loading...")
        sleep(self.sleep)  # 等待页面加载

        self.browser_source = self.browser.page_source  # 获取页面源码
        self.browser.quit()
        return True, "Get browser source successfully"

    def get_information(self, regex):
        """
        通过正则表达式获取信息

        :param regex: 正则表达式
        :return: list
        """
        if self.browser_source is None:
            raise Exception("Please call get_browser_source() first")
        print("Getting information...")
        return re.findall(regex, self.browser_source)  # 正则匹配获取信息

    def get_capacity(self):
        """
        获取容量信息

        :return: boolean, string
        """
        reg = '(?<=span style="color:white; white-space:nowrap;" class="ng-binding ng-scope">).*GB'
        res = self.get_information(reg)
        if len(res) == 0:
            return False, "Get capacity failed"
        else:
            return True, res[0]


if __name__ == '__main__':
    T = TeraCloud(input("Username: "), input("Password: "), debug=False)
    flag, message = T.get_browser_source()
    print(message)
    if flag:
        flag, message = T.get_capacity()
        if flag:
            print("Capacity: " + message)
        else:
            print(message)
