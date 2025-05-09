from selenium.webdriver.common.by import By

class Pages:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)