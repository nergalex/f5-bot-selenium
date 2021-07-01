import time
import unittest
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from twocaptcha import TwoCaptcha
# import asyncio
# import concurrent.futures
import pprint


class Flow1(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--ignore-urlfetcher-cert-requests")
        options.add_experimental_option('w3c', False)

        self.driver = webdriver.Chrome(
            executable_path=PATH,
            options=options
        )

    def test_login(self):
        self.driver.get(URI)

        # Move
        TouchActions(self.driver).scroll(10, 10).perform()

        # GET Accept data privacy
        element_id = "popin_tc_privacy_button_3"
        try:
            WebDriverWait(self.driver, 2).until(
                expected_conditions.presence_of_element_located((By.ID, element_id))
            )
        except TimeoutException:
            print("Oops!  Too long to retrieve element '%s'.  Try again..." % element_id)
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("Oops!  There is no valid element '%s'.  Try again..." % element_id)

        # Accept data privacy
        time.sleep(1.12345)
        element.click()

        # GET login
        element_id = "j_username"
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("Oops!  There is no valid element '%s'.  Try again..." % element_id)

        # SET login
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
        element_id = "j_password"
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("Oops!  That was no valid element '%s'.  Try again..." % element_id)

        # SET password
        element.clear()
        string = []
        string[:0] = LOGIN_PASSWORD
        for character in string:
            element.send_keys(character)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)

        # GET captcha image
        self.driver.switch_to.frame("mtcaptcha-iframe-1")
        element_id = "mtcap-image-1"
        captcha_exist = True
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("No CAPTCHA!  That was no valid element '%s'.  Try again..." % element_id)
            captcha_exist = False

        # Solve captcha
        if captcha_exist:
            pprint.pprint("https://onlinepngtools.com/convert-base64-to-png : %s" % element.screenshot_as_base64)
            try:
                # captcha_result = Maif.captchaSolver(image=element.screenshot_as_base64)
                captcha_result = solver.normal(
                        element.screenshot_as_base64,
                        numeric=0,
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
        element_id = "mtcap-inputtext-1"
        if captcha_exist:
            try:
                element = self.driver.find_element_by_id(element_id)
            except NoSuchElementException:
                print("No CAPTCHA input field?!  That was no valid element '%s'" % element_id)

        # SET captcha
        element.clear()
        string = []
        string[:0] = captcha_result['code']
        for character in string:
            element.send_keys(character)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)

        # submit
        self.driver.switch_to.default_content()
        interval = random.uniform(0.5, 1)
        time.sleep(interval)
        self.driver.find_element_by_id("submit-login").click()

        # Check successful login
        element_class = "error-message"
        unknown_credential = True
        try:
            element = WebDriverWait(self.driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_class))
            )
        except TimeoutException:
            print("Successful login. No element '%s' " % element_class)
            unknown_credential = False

        # Check Shape mitigation
        element_class = "page-title"
        shape_mitigation = True
        try:
            element = self.driver.find_element_by_class_name(element_class)
        except NoSuchElementException:
            shape_mitigation = False
            print("No Shape mitigation. No element '%s' " % element_id)
        if element is not None and element.text == "Demo | Blocked by Shape | Demo":
            print("Shape mitigation: %s" % element.text)

        # Check error message
        if unknown_credential and not shape_mitigation:
            print("Unknown credential by system '%s'. Try another credential..." % element.text)

    def tearDown(self):
        self.driver.close()

    # @staticmethod
    # async def captchaSolver(image):
    #     loop = asyncio.get_running_loop()
    #     with concurrent.futures.ThreadPoolExecutor() as pool:
    #         result = await loop.run_in_executor(
    #             pool,
    #             lambda: solver.normal(
    #                 image,
    #                 numeric=0,
    #                 minLength=4,
    #                 maxLength=4,
    #                 phrase=0,
    #                 caseSensitive=0,
    #                 calc=0
    #             )
    #         )
    #     return result


if __name__ == "__main__":
    PATH = "./_files/chromedriver.exe"
    LOGIN_EMAIL = "demo@hotmail.com"
    LOGIN_PASSWORD = "demo@hotmail.com!"
    URI = "YourINPUT"
    CAPTCHA_API_KEY = "YourINPUT"
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

