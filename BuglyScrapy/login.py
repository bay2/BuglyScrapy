from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

class BuglyLogin(object):

    def __init__(self):
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(desired_capabilities=caps, chrome_options=chrome_options)
        self.driver.implicitly_wait(10)
        
        pass

    def login(self, userName, passWord):

        self.driver.get("https://bugly.qq.com/v2/")
        self.driver.find_element_by_link_text("登录").click()
        self.driver.switch_to_frame("ptlogin_iframe")
        self.driver.find_element_by_link_text("帐号密码登录").click()

        # print(self.driver.page_source)

        # print('wait 30s')
        # time.sleep(30)

        print(self.driver.page_source)

        self.driver.find_element_by_id("u").send_keys(userName)
        self.driver.find_element_by_id("p").send_keys(passWord)
        self.driver.find_element_by_id("login_button").click()
        
        pass

    def get_cookies(self):
        return self.driver.get_cookies()

    def get_header(self, url):
        logs = self.driver.get_log('performance')
        entrys = map(
            lambda entry: entry['params']['request'],
            filter(
                lambda entry: entry['method'] == 'Network.requestWillBeSent', 
                list(
                    map(
                    lambda log : json.loads(log['message'])['message'], 
                    logs)
                    )
                )
            )

        for entry in entrys:
            if entry['url'].startswith(url):
                return entry['headers']

        return {}


def main():
    bugly = BuglyLogin()
    bugly.login("382499488", "/wa+fnq3DKJrJ(6")
    time.sleep(10)
    print(bugly.get_header('https://bugly.qq.com/v2/users/null/appList'))
    
 

if __name__ == "__main__":
    main()
