from selenium import webdriver
class WebAutoFramework(object):
    def __init__(self):
        self.driver = None
        if self.driver is None:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(5)

    def open(self, url):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()

    def get_title(self):
        return self.driver.title