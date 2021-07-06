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


class Flow1(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--ignore-urlfetcher-cert-requests")
        options.add_argument("--show-taps")
        options.add_argument("--auto-open-devtools-for-tabs")
        options.add_experimental_option('w3c', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(
            executable_path=PATH,
            options=options
        )
        print(self.driver.execute_script("return navigator.userAgent;"))

    def test_login(self):
        self.driver.get(URI)

        # Move
        TouchActions(self.driver).scroll(10, 10).perform()

        # GET login
        element_id = "input-1"
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
        element_id = "input-2"
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

        # submit
        element_class = "btn-primary"
        try:
            element = self.driver.find_element_by_class_name(element_class)
        except NoSuchElementException:
            print("Oops!  That was no valid element '%s'" % element_class)
        interval = random.uniform(0.5, 1)
        time.sleep(interval)
        ActionChains(self.driver).move_to_element(element).pause(interval).click(element).perform()

        # CHECK successful login
        element_class = "d-xl-inline-block"
        successful_login = True
        try:
            element = WebDriverWait(self.driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_class))
            )
        except TimeoutException:
            successful_login = False

        # SHOW result
        if successful_login:
            print("Successful login!")
        else:
            print("Unknown credential by system or mitigated by Shape. Check /v1/login response in Dev Tool")

        time.sleep(1000)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    PATH = "./_files/chromedriver.exe"
    LOGIN_EMAIL = "INPUT"
    LOGIN_PASSWORD = "INPUT"
    URI = "https://arcadia-crypto1.f5app.dev/login"

    unittest.main()







