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
import pprint


class Flow1(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--auto-open-devtools-for-tabs")
        options.add_argument("--show-taps")
        options.add_experimental_option('w3c', False)

        self.driver = webdriver.Chrome(
            executable_path=PATH,
            options=options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        print(self.driver.execute_script("return navigator.userAgent;"))

    def test_login(self):
        self.driver.get(URI)

        # Move
        TouchActions(self.driver).scroll(10, 10).perform()

        # GET Accept data privacy
        element_id = "accept_cookies_btn"
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

        # Accept data privacy
        interval = random.uniform(1.1, 1.5)
        time.sleep(interval)
        ActionChains(self.driver).move_to_element(element).pause(interval).click(element).perform()
        # element.click()

        # Click Connect
        element_name = "bwc-logo-header__login-button"
        try:
            element = self.driver.find_element_by_class_name(element_name)
        except NoSuchElementException:
            print("Oops!  There is no valid element '%s'" % element_name)
        interval = random.uniform(1.1, 1.5)
        time.sleep(interval)
        ActionChains(self.driver).move_to_element(element).pause(interval).click(element).perform()

        # GET login
        element_id = "mat-input-0"
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

        # SET login
        interval = random.uniform(1.1, 1.5)
        time.sleep(interval)
        ActionChains(self.driver).move_to_element(element).pause(interval).click(element).perform()
        element.clear()
        string = []
        string[:0] = LOGIN_EMAIL
        for character in string:
            element.send_keys(character, Keys.ARROW_DOWN)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)

        # Move
        TouchActions(self.driver).tap(element).perform()
        TouchActions(self.driver).flick_element(
            on_element=element,
            xoffset=100,
            yoffset=100,
            speed=100
        ).perform()

        # GET password
        element_id = "mat-input-1"
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("Oops!  That was no valid element '%s'" % element_id)

        # SET password
        interval = random.uniform(1.1, 1.5)
        time.sleep(interval)
        ActionChains(self.driver).move_to_element(element).pause(interval).click(element).perform()
        element.clear()
        string = []
        string[:0] = LOGIN_PASSWORD
        for character in string:
            element.send_keys(character)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)

        # GET captcha image
        element_class = "asfc-svg-captcha"
        captcha_exist = True
        try:
            element = self.driver.find_element_by_class_name(element_class)
        except NoSuchElementException:
            print("No CAPTCHA!  That was no valid element class '%s'" % element_id)
            captcha_exist = False

        # Solve captcha
        if captcha_exist:
            self.solveCaptcha(
                element_image=element,
                element_class_input="login-captcha"
            )

        # submit
        element_class = "login-form-continue-btn"
        try:
            element = self.driver.find_element_by_class_name(element_class)
        except NoSuchElementException:
            print("Oops!  That was no valid element '%s'" % element_class)
        interval = random.uniform(0.5, 1)
        time.sleep(interval)
        ActionChains(self.driver).move_to_element(element).pause(interval).click(element).perform()

        # Check asking for CAPTCHA
        element_class = "asfc-svg-captcha"
        captcha_exist = True
        try:
            element = WebDriverWait(self.driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_class))
            )
        except TimeoutException:
            print("Successful login. No element '%s' " % element_class)
            captcha_exist = False

        # Solve captcha
        if captcha_exist:
            self.solveCaptcha(
                element_image=element,
                element_class_input="login-captcha"
            )

            # submit
            element_class = "login-form-continue-btn"
            try:
                element = self.driver.find_element_by_class_name(element_class)
            except NoSuchElementException:
                print("Oops!  That was no valid element '%s'" % element_id)
            interval = random.uniform(0.5, 1)
            time.sleep(interval)
            ActionChains(self.driver).move_to_element(element).pause(interval).click(element).perform()

        time.sleep(1000)

    def tearDown(self):
        self.driver.close()

    def solveCaptcha(self, element_image, element_class_input):
        pprint.pprint("https://onlinepngtools.com/convert-base64-to-png : %s" % element_image.screenshot_as_base64)
        try:
            captcha_result = solver.normal(
                element_image.screenshot_as_base64,
                numeric=1,
                minLength=4,
                maxLength=4,
                phrase=0,
                caseSensitive=0,
                calc=0
            )
        except Exception as e:
            print("2CAPTCHA error %s" % e['args'][0])
        print("2CAPTCHA - solved: '%s' " % captcha_result['code'])

        # GET captcha input field
        try:
            element = self.driver.find_element_by_class_name(element_class_input)
        except NoSuchElementException:
            print("No CAPTCHA input field?!  That was no valid element class '%s'" % element_class_input)
        
        # SET captcha input field
        interval = random.uniform(1.1, 1.5)
        time.sleep(interval)
        ActionChains(self.driver).move_to_element(element).pause(interval).click(element).pause(interval).perform()
        element.clear()
        string = []
        string[:0] = captcha_result['code']
        for character in string:
            element.send_keys(character)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)


if __name__ == "__main__":
    PATH = "./_files/chromedriver.exe"
    LOGIN_EMAIL = "INPUT"
    LOGIN_PASSWORD = "INPUT"
    URI = "INPUT"
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

