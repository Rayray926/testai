from time import sleep
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from openai import BaseModel
from pydantic import Field

class AppAutoFrameworkTools:
    def __init__(self):
        self.driver = None
        self.element = None

    def init(self, app_activity, app_package):
        if not self.driver:
            caps = {
                "platformName": "android",
                "appium:automationName": "uiautomator2",
                "appium:deviceName": "HIEM657P5X6PQCNZ",
                "appium:noReset": True,
                "appium:forceAppLaunch" : True,
                "appium:shouldTerminateApp" : True,
                "appium:newCommandTimeout":600,
                "appium:appPackage": "com.android.settings",
                "appium:appActivity": ".Settings"
            }
            # 初始化 driver
            self.driver = webdriver.Remote(
                "http://localhost:4723/wd/hub",
                options=UiAutomator2Options().load_capabilities(caps)
            )
            self.driver.implicitly_wait(5)
        return self.source()

    def source(self):
        return self.driver.page_source

    def find(self, locator):
        print(f"find xpath = {locator}")
        element = self.driver.find_element(by=AppiumBy.XPATH, value=locator)
        self.element = element
        return self.source()

    def click(self):
        self.element.click()
        sleep(1)
        return self.source()

    def send_keys(self, text):
        self.element.clear()
        self.element.send_keys(text)
        return self.source()

    def back(self):
        self.driver.back()
        return self.source()


import time

from langchain_core.tools import tool

app = AppAutoFrameworkTools()


@tool
def init(app_activity, app_package):
    """
    打开app的安装包，并返回app的resource
    """
    return app.init(app_activity, app_package)


@tool
def find(xpath: str):
    """通过xpath定位元素"""
    return app.find(xpath)


@tool
def click(xpath: str = None):
    """以xpath的方式定位网页元素后点击"""
    app.find(xpath)
    return app.click()


@tool
def send_keys(xpath, text):
    """定位到xpath指定的元素，并输入text"""
    app.find(xpath)
    return app.send_keys(text)


@tool
def sleep(seconds: int):
    """等待指定的秒数"""
    time.sleep(seconds)


@tool
def back():
    """
    返回上一级界面
    :return:
    """
    app.back()


tools = [init, find, click, send_keys, sleep, back]