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

        # GET login
        element_id = "j_username"
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
            print("Oops!  That was no valid element '%s'" % element_id)

        # SET password
        element.clear()
        string = []
        string[:0] = LOGIN_PASSWORD
        for character in string:
            element.send_keys(character)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)

        # submit
        # element.send_keys(Keys.RETURN)
        interval = random.uniform(0.5, 1)
        time.sleep(interval)
        self.driver.find_element_by_class_name("login-button").click()

        # Check successful login
        element_class = "js-msg"
        unknown_credential = False
        try:
            element = WebDriverWait(self.driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_class))
            )
        except TimeoutException:
            unknown_credential = True

        # Check Shape mitigation
        if unknown_credential:
            element_class = "page-title"
            try:
                element = self.driver.find_element_by_class_name(element_class)
            except TimeoutException:
                print("Oops!  That was no valid element '%s'" % element_id)
            if element.text == "Demo | Blocked by Shape | Demo":
                print("Shape mitigation: %s" % element.text)
            else:
                print("Oops!  unknown element '%s'. Review code" % element_id)

        else:
            print("Unknown credential by system '%s', value '%s'. Try another credential..." % (element_class, element.text))

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    PATH = "./_files/chromedriver.exe"
    LOGIN_EMAIL = "demo@hotmail.com"
    LOGIN_PASSWORD = "demo@hotmail.com!"
    URI = "YourINPUT"

    unittest.main()

