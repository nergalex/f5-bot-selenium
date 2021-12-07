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
        global URI, LOGIN_USER, LOGIN_PASSWORD, CAPTCHA_API_KEY, solver, URI_INFO_PERSO, USER_AGENT, URI_CONTRAT
        URI = "INPUT"
        URI_INFO_PERSO = "INPUT"
        URI_CONTRAT = "INPUT"
        LOGIN_USER = "INPUT"
        LOGIN_PASSWORD = "INPUT"
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
        self.driver.get(URI)
        time.sleep(15)

        # Check presence of GeeTest
        element = self.getElementTagName("script")[1]
        uri_parsed = urlparse.urlparse(element.get_attribute("src"))
        if uri_parsed.hostname == 'ct.captcha-delivery.com':
            self.workflowSolveGeetest()

        # Accept data privacy
        element = self.getElementId("onetrust-accept-btn-handler")
        self.clickButton(element)

        # Open menu
        element = self.getElementId("btnVosEspaceOpen")
        self.clickButton(element)

        # Open Espace Assurance
        element = self.getElementClass("mcf-h3")
        self.clickButton(element)
        time.sleep(12)

        # Check presence of GeeTest
        element = self.getElementTagName("script")[1]
        # element = self.getElementTagName("iframe")
        if element is not None:
            uri_parsed = urlparse.urlparse(element.get_attribute("src"))
            # if uri_parsed.hostname == 'geo.captcha-delivery.com':
            if uri_parsed.hostname == 'ct.captcha-delivery.com':
                self.workflowSolveGeetest()
                time.sleep(5)

        # Login
        element = self.getElementId("login")
        self.setForm(element=element, input_data=LOGIN_USER)

        # Submit
        element = self.getElementClass("mcf-btn--lg")
        self.clickButton(element)

        # Password
        element = self.getElementId("password")
        self.setForm(element=element, input_data=LOGIN_PASSWORD)

        # Submit
        element = self.getElementClass("mcf-btn--lg")
        self.clickButton(element)
        time.sleep(3)

        # Check GeeTest
        element = self.getElementTagName("script")[1]
        uri_parsed = urlparse.urlparse(element.get_attribute("src"))
        if uri_parsed.hostname == 'ct.captcha-delivery.com':
            self.workflowSolveGeetest()

        # Go to info perso
        time.sleep(5)
        self.driver.get(URI_INFO_PERSO)
        time.sleep(5)

        # Check presence of GeeTest
        element = self.getElementTagName("script")[1]
        uri_parsed = urlparse.urlparse(element.get_attribute("src"))
        if uri_parsed.hostname == 'ct.captcha-delivery.com':
            self.workflowSolveGeetest()
            time.sleep(5)

        # Mon Profil
        elements = self.driver.find_elements_by_class_name("epi-sub-title")

        # Data leak
        print("personal info leaked:")
        for index, element in enumerate(elements):
            print("- %s" % element.text)

        time.sleep(1000)

        # Go to contrat
        # self.driver.get(URI_CONTRAT)
        # time.sleep(2)

        # Check presence of GeeTest
        # element = self.getElementTagName("script")[1]
        # uri_parsed = urlparse.urlparse(element.get_attribute("src"))
        # if uri_parsed.hostname == 'ct.captcha-delivery.com':
        #     self.workflowSolveGeetest()

        # Contracts
        # elements_contract_type = self.driver.find_elements_by_class_name("epi-title")
        #
        # print("contract leaked:")
        # contract_enumerate = len(elements_contract_type)
        # for index_contract in range(0, contract_enumerate):
        #     # Go to contract
        #     elements_contract_name = self.driver.find_elements_by_class_name("epi-subtitle")
        #     print("- contract %s:  %s" % (
        #         elements_contract_type[index_contract].text, elements_contract_name[index_contract].text))
        #     self.clickButton(elements_contract_type[index_contract])
        #     time.sleep(2)
        #
        #     # Get fee
        #     element = self.getElementClass("annual-fee")
        #     print("   +-- annual-fee:  %s" % element.text)
        #
        #     # Get info
        #     elements_label = self.driver.find_elements_by_class_name("title")
        #     elements_value = self.driver.find_elements_by_class_name("value")
        #
        #     for index2, label in enumerate(elements_label):
        #         print("   +-- %s: %s" % (label.text, elements_value[index2].text))
        #
        #     # Go back
        #     self.driver.get(URI_CONTRAT)
        #     time.sleep(2)
        #     elements_contract_type = self.driver.find_elements_by_class_name("epi-title")

    def workflowSolveGeetest(self):
        # Move
        moove_cursor = ActionChains(self.driver)
        previous_x = 0
        previous_y = 0
        target_x = 150
        target_y = 800

        for i in range(1, 100):
            previous_x = random.uniform(previous_x, target_x)
            previous_y = random.uniform(previous_y, target_y)
            moove_cursor = moove_cursor.move_by_offset(previous_x, previous_y)
        moove_cursor.perform()

        # GET GeeTest specifications
        geetest = self.getCurrentGeeTest()

        # GET a new GeeTest challenge
        geetest['challenge'] = self.getNewGeeTestChallenge(geetest['url'])

        # SOLVE
        geetest_result = self.solveGeeTest(
            gt=geetest['gt'],
            challenge=geetest['challenge'],
            url=geetest['url']
        )

        # SET GeeTest
        self.setGeeTestResult(geetest_result)

    def getNewGeeTestChallenge(self, url):
        challenge = ''
        r = self.session.get(url=url, verify=False)

        for line in r.text.split('\n'):
            result = re.findall(r"^\s*challenge:\s'(.*)',$", line)
            if len(result) != 0:
                challenge = result[0]
        return challenge

    def solveGeeTest(self, gt, challenge, url):
        print("2CAPTCHA - GeeTest")
        print("  gt: '%s' " % gt)
        print("  challenge: '%s' " % challenge)
        print("  url: %s " % url)

        # SOLVE via TwoCaptcha class
        print("2CAPTCHA via TwoCaptcha class - try to solve, please wait a minute...")
        captcha_result = None
        try:
            captcha_result = solver.geetest(
                gt=gt,
                challenge=challenge,
                url=url,
                api_server="api-na.geetest.com"
            )
        except Exception as e:
            print("2CAPTCHA via TwoCaptcha class - error %s" % e.args[0])

        print("2CAPTCHA - GeeTest solved:")
        pprint.pprint(json.loads(captcha_result["code"]))
        return json.loads(captcha_result["code"])

        # SOLVE via API
        # data = {
        #     "key": CAPTCHA_API_KEY,
        #     "method": "geetest",
        #     "gt": gt,
        #     "challenge": challenge,
        #     "api_server": "api-na.geetest.com",
        #     "pageurl": url,
        #     "json": 1,
        #     "userAgent": USER_AGENT
        # }
        # r_post = self.session.post(url="http://2captcha.com/in.php", data=data)
        # if r_post.status_code != requests.codes.ok:
        #     print("error ajax: %s %s" % (r_post.status_code, r_post.text))
        #     raise

        # wait
        # print("2CAPTCHA via API - try to solve, please wait a minute...")
        # time.sleep(45)

        # GET results
        # request_id = json.loads(r_post.text)['request']
        # url_result = "http://2captcha.com/res.php?" + \
        #              "key=" + CAPTCHA_API_KEY + \
        #              "&action=get" + \
        #              "&id=" + request_id + \
        #              "&json=1"
        # r_get = self.session.get(url_result)
        # if r_get.status_code != requests.codes.ok:
        #     print("error ajax: %s %s" % (r_get.status_code, r_get.text))
        #     raise
        # else:
        #     print("2CAPTCHA - GeeTest solved:")
        #     pprint.pprint(json.loads(r_get.text)['request'])
        #     return json.loads(r_get.text)['request']

    def setGeeTestResult(self, geetest):
        # SEND a message to iframe in order to launch Callback
        post_message_data = "geeTestCallback=" + str(geetest['geetest_challenge']) \
                            + '=' + str(geetest['geetest_validate']) \
                            + '=' + str(geetest['geetest_seccode'])
        js_script = "iframe = document.getElementsByTagName('iframe')[0]; " + \
                    "iframe.contentWindow.postMessage('" + \
                    post_message_data + \
                    "', '*');"
        self.driver.execute_script(js_script)

    def getCurrentGeeTest(self):
        # ------ BIG-IP ------
        # HTML profile "grecaptcha" attached to Reverse-Proxy
        # Content-Type Selection: text/html + text/xhtml
        # HTML rule geo.captcha-delivery.com_postMessage
        # +-- Match Tag Name: body
        # +-- HTML to Append: cf. iframe_cors_bypass-listener.js

        # Inject client to receive message from frame geo.captcha and set attribute title
        js_script = "function receiveMessage(event) { " + \
                    "iframe = document.getElementsByTagName('iframe')[0]; " + \
                    "server = event.data.split('/')[2].split('&')[0]; " + \
                    "gt = event.data.split('=')[1].split('&')[0]; " + \
                    "challenge = event.data.split('=')[2].split('&')[0]; " + \
                    "iframe.setAttribute(name='server', server);" + \
                    "iframe.setAttribute(name='gt', gt);" + \
                    "iframe.setAttribute(name='challenge', challenge);" + \
                    "} " + \
                    "window.addEventListener('message', receiveMessage, false);"

        self.driver.execute_script(js_script)

        # SEND a message to iframe in order to receive challenge back
        js_script = "iframe = document.getElementsByTagName('iframe')[0]; " + \
                    "iframe.contentWindow.postMessage('geeTestGetChallenge', '*');"
        self.driver.execute_script(js_script)

        # get challenge
        data = {}
        time.sleep(1)
        frame = self.getElementTagName("iframe")[0]
        data['gt'] = frame.get_attribute("gt")
        data['challenge'] = frame.get_attribute("challenge")
        data['api_server'] = frame.get_attribute("server")
        data['url'] = frame.get_attribute("src")
        return data

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
