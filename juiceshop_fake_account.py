import time
import unittest
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from twocaptcha import TwoCaptcha
import urllib.parse as urlparse
from urllib.parse import parse_qs
import json
import requests
import re
import random
import string


class Flow1(unittest.TestCase):

    def setUp(self):
        global BASE_PATH, LOGIN_USER, LOGIN_PASSWORD, CAPTCHA_API_KEY, solver, USER_AGENT, random_email, random_password
        BASE_PATH = "https://hostname_here/"

        # local
        PATH = "./_files/chromedriver.exe"
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"

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

    def test_create_user(self):
        self.session = requests.session()

        # goto welcome page
        uri_login = BASE_PATH + "/#/register"
        self.driver.get(uri_login)
        time.sleep(1)

        # Data Privacy
        element = self.driver.find_elements_by_class_name("close-dialog")[0]
        self.clickButton(element)

        # Cookie warning
        element = self.driver.find_elements_by_class_name("cc-dismiss")[0]
        self.clickButton(element)

        while True:

            # generate random credentials
            password_characters = string.ascii_letters + string.digits + string.punctuation
            random_email = f"{self.get_random_string() + '@gmail.com'}"
            random_password = ''.join(random.choice(password_characters) for i in range(10))

            # Move
            TouchActions(self.driver).scroll(0, 30).perform()
            # email
            element = self.getElementId("emailControl")
            self.setForm(element=element, input_data=random_email)
            # password
            element = self.getElementId("passwordControl")
            self.setForm(element=element, input_data=random_password)
            # repeated password
            element = self.getElementId("repeatPasswordControl")
            self.setForm(element=element, input_data=random_password)
            # Security Question drop down list
            element = self.getElementId("mat-select-value-1")
            element.click()
            element = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/mat-option[2]/span")
            element.click()
            # Security answer
            element = self.getElementId("securityAnswerControl")
            self.setForm(element=element, input_data=random_password)
            # Submit
            element = self.getElementId("registerButton")
            self.clickButton(element)
            time.sleep(0.1)

            # go back to register page
            uri_login = BASE_PATH + "/#/register"
            self.driver.get(uri_login)
            time.sleep(0.1)

    def get_random_string(self):
        length = 10

        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def tearDown(self):
        self.driver.close()

    def clickButton(self, element):
        interval_think = random.uniform(0.5, 0.8)
        interval_get_mouse = random.uniform(0.5, 0.8)
        interval_click = random.uniform(0.1, 0.3)
        offset_x = random.uniform(1, 3)
        offset_y = random.uniform(1, 3)

        ActionChains(self.driver).pause(interval_think). \
            move_by_offset(offset_x, offset_y). \
            move_to_element(element).pause(interval_get_mouse). \
            click_and_hold(element).pause(interval_click).release(element). \
            perform()

    def setForm(self, element, input_data):
        interval_think = random.uniform(0.5, 0.8)
        interval_get_mouse = random.uniform(0.5, 0.8)
        interval_click = random.uniform(0.1, 0.3)
        offset_x = random.uniform(50, 100) * -1
        offset_y = random.uniform(50, 100) * -1

        ActionChains(self.driver).pause(interval_think). \
            move_by_offset(offset_x, offset_y). \
            move_to_element(element).pause(interval_get_mouse). \
            click_and_hold(element).pause(interval_click).release(element). \
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


if __name__ == "__main__":
    unittest.main()
