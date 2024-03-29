import pprint
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
import urllib.parse as urlparse
from urllib.parse import parse_qs
import json
import requests
import re


class Flow1(unittest.TestCase):

    def setUp(self):
        global URI, LOGIN_USER, LOGIN_PASSWORD, LOGIN_BIRTHDAY, CAPTCHA_API_KEY, solver, USER_AGENT
        URI = "INPUT"
        LOGIN_USER = "INPUT"
        LOGIN_PASSWORD = "INPUT"
        LOGIN_BIRTHDAY = "INPUT"
        CAPTCHA_API_KEY = "INPUT"

        # local
        PATH = "./_files/chromedriver.exe"
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"

        config = {
            'server': '2captcha.com',
            'apiKey': CAPTCHA_API_KEY,
            'softId': 1,
            'defaultTimeout': 120,
            'recaptchaTimeout': 600,
            'pollingInterval': 10,
        }
        solver = TwoCaptcha(**config)

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
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": USER_AGENT})
        print("Run Selenium bot with User Agent: %s" % self.driver.execute_script("return navigator.userAgent;"))

    def test_login(self):
        self.session = requests.session()

        # goto welcome page
        self.driver.get(URI)
        time.sleep(3)

        # Accept data privacy
        element = self.getElementId("popin_tc_privacy_button_2")
        self.clickButton(element)

        # User account
        element = self.getElementClass("icon-header-user")
        self.clickButton(element)

        # Login
        element = self.getElementId("wsi-login-credentials-form-email-input-input")
        self.setForm(element=element, input_data=LOGIN_USER)

        # Password
        element = self.getElementId("wsi-login-credentials-form-password-input-input")
        self.setForm(element=element, input_data=LOGIN_PASSWORD)

        # Birth date
        element = self.getElementId("wsi-login-credentials-form-birthdate-input-input")
        self.setForm(element=element, input_data=LOGIN_BIRTHDAY)

        # Submit
        element = self.getElementId("wsi-authenticate-button")
        self.clickButton(element)
        time.sleep(1)

        # Skip
        # element = self.getElementId("wsi-post-authentication-skip-optional-layers")
        # if element is not None:
        #     self.clickButton(element)
        #     time.sleep(1)

        # MyAccount
        element = self.getElementClass("main-nav_connect-user_myaccount")
        self.clickButton(element)
        time.sleep(1)

        # Retrait
        element = self.getElementId("wsi-connected-layer-summary-wallets-withdrawal-button")
        self.clickButton(element)
        time.sleep(1)

        # Completer
        element = self.getElementClass("action-link-btFournirMapiece-origin")
        self.clickButton(element)
        time.sleep(1)

        # IBAN
        element = self.getElementId("ibanNumber")
        IBAN = "12345678901234567890"
        self.setForm(element=element, input_data=IBAN)

        # GET gain
        element = self.getElementClass("main-nav_connect-user_infos-amount")
        GAIN = element.text.split(' ')

        # Virement
        element = self.driver.find_elements_by_class_name("ng-pristine")[2]
        element.clear()
        self.setForm(element=element, input_data=GAIN)

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

        return captcha_result['code']


if __name__ == "__main__":

    unittest.main()
