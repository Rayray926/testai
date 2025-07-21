import time

from langchain_core.tools import tool
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebAutoFrameworkTools:

    def __init__(self):
        self.driver = None
        self.element = None

    def init(self):
        if not self.driver:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(5)

    def open(self, url):
        self.init()

        self.driver.get(url)
        return self.source()

    #用于获取网页中所有<button>和<input>元素的HTML内容，并返回拼接后的字符串
    def source(self):
        return self.driver.execute_script(
            """
            var content="";
            document.querySelectorAll('button').forEach(x=> content+=x.outerHTML);
            document.querySelectorAll('input').forEach(x=> content+=x.outerHTML);
            //document.querySelectorAll('table').forEach(x=> content+=x.outerHTML);
            return content;
            """
        )

    def click(self):
        """
        点击当前的元素
        :return:
        """
        self.element.click()
        sleep.invoke({"seconds": 1})
        return self.source()

    def send_keys(self, text):
        self.element.clear()
        self.element.send_keys(text)
        return self.source()

    def find(self, locator):
        print(f"find css = {locator}")
        element = self.driver.find_element(by=By.CSS_SELECTOR, value=locator)
        self.element = element
        return self.source()

    def quit(self):
        self.driver.quit()

    def get_current_url(self):
        print(f"当前的url为{self.driver.current_url}")
        return self.driver.current_url

web = WebAutoFrameworkTools()
@tool
def open(url: str):
    """
    使用浏览器打开特定的url，并返回网页内容
    """
    r = web.open(url)
    return r

@tool
def find(css: str):
    """定位网页元素"""
    return web.find(css)

@tool
def click(css: str = None):
    """以css的方式定位网页元素后点击"""
    web.find(css)
    return web.click()

@tool
def send_keys(css, text):
    """定位到css指定的元素，并输入text"""
    web.find(css)
    return web.send_keys(text)

@tool
def sleep(seconds: int):
    """等待指定的秒数"""
    time.sleep(seconds)


@tool
def quit():
    """退出浏览器"""
    web.quit()

@tool
def get_current_url():
    """获取当前的url"""
    return web.get_current_url()

tools = [open, get_current_url, find, click, send_keys,quit]



