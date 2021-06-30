import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class PythonOrgSearch(unittest.TestCase):

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

    def test_airgas_login(self):
        self.driver.get("https://www.airgas.com/login")
        login_email = "demo@hotmail.com"
        login_password = "demo@hotmail.com!"

        # Move
        TouchActions(self.driver).scroll(10, 10).perform()

        # login
        element_id = "j_username"
        try:
            WebDriverWait(self.driver, 2).until(
                expected_conditions.presence_of_element_located((By.ID, element_id))
            )
        except TimeoutException:
            print("Oops!  Too long to retrieve element '%s'.  Try again..." % element_id)
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("Oops!  That was no valid element '%s'.  Try again..." % element_id)
        element.clear()
        element.send_keys(login_email, Keys.ARROW_DOWN)

        # Move
        TouchActions(self.driver).tap(element).perform()
        TouchActions(self.driver).flick_element(element, 100, 100, 50).perform()

        # password
        element_id = "j_password"
        try:
            element = self.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            print("Oops!  That was no valid element '%s'.  Try again..." % element_id)
        element.clear()
        element.send_keys(login_password, Keys.PAGE_UP)

        # submit
        # element.send_keys(Keys.RETURN)
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

        if unknown_credential:
            # Check Shape mitigation
            element_class = "page-title"
            try:
                element = self.driver.find_element_by_class_name(element_class)
            except TimeoutException:
                print("Oops!  That was no valid element '%s'. Review code" % element_id)
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

    unittest.main()

# ChromeDriver response in W3C mode is not standard compliant
### https://bugs.chromium.org/p/chromedriver/issues/detail?id=1942
# https://developers.perfectomobile.com/display/TT/How+to+pass+Chrome+options+as+capabilities