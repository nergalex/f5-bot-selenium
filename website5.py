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
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        print("Run Selenium bot with User Agent: %s" % self.driver.execute_script("return navigator.userAgent;"))

    def test_login(self):
        self.driver.get(URI)

        # Move
        TouchActions(self.driver).scroll(10, 10).perform()

        # Accept data privacy
        element = self.getElementId("onetrust-accept-btn-handler")
        self.clickButton(element)

        # Connect
        element = self.getElementId("ctl00_ucWPAD007_ConnexionDrive_divWPAD346_NonConnecte")
        self.clickButton(element)

        # Login
        element = self.getElementId("ctl00_ucWPAD007_ConnexionDrive_ctl00_txtWCLD312_Login")
        self.clickButton(element)
        self.setForm(element=element, input_data=LOGIN_EMAIL)

        # Continue
        element_previous = element
        element = self.getElementClass("btnWCLD312_Continuer")
        self.clickButton(element)

        # Password
        time.sleep(1)
        element_previous = element
        element = self.getElementId("ctl00_ucWPAD007_ConnexionDrive_ctl00_txtWCLD312_Mdp")
        self.clickButton(element)
        self.setForm(element=element, input_data=LOGIN_PASSWORD)

        # GET captcha
        frame = self.driver.find_elements_by_tag_name("iframe")[0]
        uri_parsed = urlparse.urlparse(frame.get_attribute("src"))
        if uri_parsed.fragment == '':
            # show Shape mitigation
            time.sleep(1000)
        else:
            # hcaptcha - continue
            pass
        site_key = parse_qs(uri_parsed.fragment)['sitekey'][0]

        # Solve hcaptcha
        self.solveHCaptcha(
            site_key=site_key,
            frame=frame
        )

        # Submit
        element = self.getElementClass("btnWCLD312_Valider")
        self.clickButton(element)

        # wait for loading page
        time.sleep(5)

        # No grecaptcha
        if self.getElementClass("popinDriveMagasin__Choix") is not None:
            element = self.getElementClass("popinDriveMagasin__NomMagasin")
            print("Credential success!")
            print("personal info - prefered Drive store: %s" % element.text)
            time.sleep(1000)

        else:
            # grecaptcha - continue
            pass

        # Move
        # TouchActions(self.driver).scroll(10, 10).perform()

        # Inject client to receive message from frame geo.captcha and set attribute title
        self.driver.switch_to.default_content()
        js_script = "function receiveMessage(event) { " + \
            "iframe = document.getElementsByTagName('iframe')[3]; " + \
            "iframe.setAttribute(name='title', event.data);" + \
            "} " + \
            "window.addEventListener('message', receiveMessage, false);"
        self.driver.execute_script(js_script)

        # SEND a message to iframe in order to receive a site_key back
        js_script = "iframe = document.getElementsByTagName('iframe')[3]; " + \
                    "iframe.contentWindow.postMessage('getSiteKey', '*');"
        self.driver.execute_script(js_script)
        
        # lookup for site_key
        frame = self.driver.find_elements_by_tag_name("iframe")[3]
        uri_parsed = urlparse.urlparse(frame.get_attribute("title"))
        site_key = parse_qs(uri_parsed.query)['k'][0]

        # Solve Gcaptcha
        self.solveGRecaptcha(
            site_key=site_key,
            url=frame.get_attribute("src")
        )

        time.sleep(5)

        # Connect
        element = self.getElementId("ctl00_ucWPAD007_ConnexionDrive_divWPAD346_NonConnecte")
        self.clickButton(element)

        # Login
        element = self.getElementId("ctl00_ucWPAD007_ConnexionDrive_ctl00_txtWCLD312_Login")
        self.clickButton(element)
        self.setForm(element=element, input_data=LOGIN_EMAIL)

        # Continue
        element = self.getElementClass("btnWCLD312_Continuer")
        self.clickButton(element)

        # Password
        time.sleep(1)
        element = self.getElementId("ctl00_ucWPAD007_ConnexionDrive_ctl00_txtWCLD312_Mdp")
        self.clickButton(element)
        self.setForm(element=element, input_data=LOGIN_PASSWORD)

        # GET captcha
        frame = self.driver.find_elements_by_tag_name("iframe")[0]
        uri_parsed = urlparse.urlparse(frame.get_attribute("src"))
        site_key = parse_qs(uri_parsed.fragment)['sitekey'][0]

        # Solve hcaptcha
        self.solveHCaptcha(
            site_key=site_key,
            frame=frame
        )

        # Submit
        element = self.getElementClass("btnWCLD312_Valider")
        self.clickButton(element)

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
        element.clear()
        string = []
        string[:0] = input_data
        for character in string:
            element.send_keys(character)
            interval = random.uniform(0.1, 0.35)
            time.sleep(interval)

    def tabMove(self, repeat, enter=True):
        interval_think = random.uniform(1, 1.5)

        flow = ActionChains(self.driver).pause(interval_think)
        for i in range(0, repeat):
            flow = ActionChains(self.driver)
            interval_click = random.uniform(0.05, 0.1)
            interval_tab = random.uniform(1, 1.5)
            flow = flow.pause(interval_tab).key_down(Keys.TAB).pause(interval_click).key_up(Keys.TAB)
            flow.perform()
        if enter:
            interval_click = random.uniform(0.05, 0.1)
            flow = flow.pause(interval_think).key_down(Keys.ENTER).pause(interval_click).key_up(Keys.ENTER)
        flow.perform()

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
            return None
        return element

    def solveHCaptcha(self, site_key, frame):
        print("2CAPTCHA - hcaptcha site key: '%s' " % site_key)
        print("2CAPTCHA - try to solve, please wait a minute...")

        # captcha_result = {'code': 'P0_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiMVFoNHQ3OHkxcXZaNjdKM3ZqblZTeWJOdjE1Z2NPeGxNVVl6aXYvQXhKSUp0YUtUSHlUMUkwc0ZCOU5LZVVxNWw4Q3BmamExNkxPRWt6dmRJR3BUME5BNENNWmRvSE9ObVptZUJzRnYzMzJRVFBnVmtIRkdiRVZqckYvV0ZvVDZJWnlFeFdCbDNXUlFpM0FTaGRMR01WRnZ2ODdielB5MmNSODJnaTNPNG45NVYxeE1ZeWMzOWQ3N1QxZTNXb0RQc1d1aCtpMXhxL21yVUtnZFErMnNUV1FtYlhNbVQ5emlxUHlMNGszUkRZZE1KbWhpUFhWN3UzTko5c3B5VVV3TjhpUDl5Wk5CZnJYYWg2enhJa1hOZ2tkK3Y5NW9YRGxnc1FsYWxzSGhJTHNacnFwVTJNQmE0OXVWOFdMOWtHaEtWMEVMUFNMYlMyaTZMcTBSaFJFRlQ5NGwyMVVKaTZCRGI5Z044eitzMUNOb3pydGpFVkVlbk9BVGNWNHJhZ1AyTHlKOFYvUnhXZ3NkWC9iWG12eHhJdmZTVkp2SHkrWFFmRE1sOUJ2SXpDdDlHS0FLcmZGT1RKTU5uWDFhVUJhVmVQV2VrZUtqd1Y0akdvTXZEdXl3RWU5RWdBOHZOYTVyZXFOOGxBQXhSNThOaURYTmUvZzRhTk5QR1oxWWtXWXVVdHgwM2ZZOXZFQ3BNZC8xN0h4eW83bmVoRmd1YTF6UHhmUGN1Mi8yY1lCdzJMT284bHNRak9ZS2QrcFl3WmgyTVFZSHBLVkFaZ3dXSUVmRHVRRjRUN0JJbkxyS3NVMThQZWVMQ1M1aDNEdmxnazZzeC9MUUhJeWZJa1R1eEovK0hFOEtzOTB1UG84ZDhEWjhRODlhUml0WE9UM1A3OFZVb0lmT3hsbVJmakVSMGJVbmd1V2htVmNiWlBVOC8zbTNGQ2RBK09lTUVKdUE2dHRXS25KUndjUXAxUTFwcUdPV0tMT3VkcmtNNEx4OFZaeUk0MTE1THRXdWpKcVA0dlhPcTJ3djRteFJGZjZEMUpwcEtBMUE4T3Y5MnI4MXNqN1g1V2Rjc3VMNFlWTjYrZnNiSVY5eUIxRHB1TW84dkJkZjVVUEtSOWYrU2gvT1BkeHZXMWZXOVpOQVVBcERObU5kMS9lNERiT25Ed1Z5OEZtNGpiTXNmSHFBYjFKNXg0TDhTM0Q2QnNTVEg0dENBRDFIU2txaUhad2JYNVFEREpQSWhTUmFDRWdZUjVCZ0NpYnNEOC9hUXYySHpOcjNjajQ4RUJLSUdxRi9sNU9BTmxGNndHeStJUWZQWnp6bXBZQmxuK3Vud0Rpanp2a0dYMWNVN0VzYzBHaHNVNE4zSnNOR0NqVlZsR2V6NUR1eDNTY0ZpdFA0N0VGOXp0dVhjZDhrM1AvTlV3MDM0ME9lak9BSktvOE1BMUxaNFJaUlJhVWNPcElic2FiRXE5RVpQMGpyTnJ5SjRmemhPV2R1WlZVdE9yTWdTY1E3TGwxcGxXaElJWmh4Zmo4Q0dmeVF0UjdkRGw5a0ZkR2pHTituaEFUMkdnSDkrVnlzM0ovdElJWjZoWmhpQTZMVEVxZkZMZGNpVlZNM2ExeXozanBwU2JrYVZhNHhVMHMwdWVZQTVVWGVtdmxHVkp3YWhJV3dqKzlhTE0wOGxNWHpEdjVBc0dCNWN4NkFQZmw3UlJyc2gxQ0ttWjJMZEhyc3Q5NEVySmI1M1YvWFRHb1l6cHhVQzRpdWtRMnNMaDUwYlo3czFuWHNxZnNBSzlDbUhUMHlEQjJmbXNkdlN3TXZ6eFo5b1hxbzZocDd6ajU1aVBZeHpXa2k3NDlOVFJJemFKTUxQOTgzVWdnbW9maHdnZmxHMlVNcVlWVEFXckM2RjVLeCs2eE5GSEhOQXg3ck1XZVhlQllTMEkwbzVVMUZSTUphb0Q0aGhWclZtTVcyMnZlS2xJYk0yUFA0c3ovdWJIM09EK1paZWl4Qm13cGVkZWhMMng0c2o4S3ZKRmYveGVhYzlaRXFNQlEzSTQyVnkvZEtqWllSTDBRaDJYQW5iNmNWL0hJRm5xckcyWmRMaksvUFpQQzNha2VNUEIzSVdNYytOaVlsS0NRVjNNZ3B1dGpYeHlncXljMFpIOXE4aEhIYSIsImV4cCI6MTYyNTk1MTUzNiwic2hhcmRfaWQiOjgyMDc4NjA4NiwicGQiOjB9.HP4Wb1SFqQ_RePhS7oPSc6fUJ8kAjxigcyfmwBTH0k8'}

        # SOLVE CAPTCHA
        try:
            captcha_result = solver.hcaptcha(
                sitekey=site_key,
                url=URI
            )
        except Exception as e:
            print("2CAPTCHA error %s" % e.args[0])
        print("2CAPTCHA - hcaptcha solved: '%s' " % captcha_result['code'])

        # OVERRIDE function
        js_script = "WCLD320_Captcha = {recupererReponseCaptcha: function(n) {return '" + \
                    captcha_result['code'] + \
                    "' }, rafraichirCaptcha: function(n) { hcaptcha.reset(n) }};"
        self.driver.execute_script(js_script, frame)

        #---------------------------- DRAFT 1 ----------------------------
        # SET frame >> hcaptcha-response
        # js_script = "document.getElementsByTagName('iframe')[0].setAttribute('data-hcaptcha-response', '" + captcha_result['code'] + "');"
        # self.driver.execute_script(js_script, frame)
        # js_script = "document.getElementsByName('h-captcha-response')[0].innerHTML='" + captcha_result['code'] + "';"
        # self.driver.execute_script(js_script, frame)
        # js_script = "document.getElementsByName('g-recaptcha-response')[0].innerHTML='" + captcha_result['code'] + "';"
        # self.driver.execute_script(js_script, frame)

        #---------------------------- DRAFT 2 ----------------------------
        # SET frame >> hcaptcha-response
        # js_script = "arguments[0].setAttribute('data-hcaptcha-response', '" + captcha_result['code'] + "');"
        # self.driver.execute_script(js_script, frame)

        # GET hcaptcha input | textarea 0
        # element_input_name = "h-captcha-response"
        # try:
        #     element = self.driver.find_element_by_name(element_input_name)
        # except NoSuchElementException:
        #     print("No CAPTCHA input field?!  That was no valid element name '%s'" % element_input_name)

        # SET hcaptcha input | textarea 0
        # self.driver.execute_script("arguments[0].setAttribute('style', 'color: Red; font-size: .8em;');", element)
        # element.clear()
        # element.send_keys(captcha_result['code'])
        # self.driver.execute_script("arguments[0].setAttribute('style', 'display: none;');", element)

        # GET recaptcha input | textarea 1
        # element_input_name = "g-recaptcha-response"
        # try:
        #     element = self.driver.find_element_by_name(element_input_name)
        # except NoSuchElementException:
        #     print("No CAPTCHA input field?!  That was no valid element name '%s'" % element_input_name)

        # SET recaptcha input | textarea 1
        # self.driver.execute_script("arguments[0].setAttribute('style', 'color: Red; font-size: .8em;');", element)
        # element.clear()
        # element.send_keys(captcha_result['code'])
        # self.driver.execute_script("arguments[0].setAttribute('style', 'display: none;');", element)

    def solveGRecaptcha(self, site_key, url):
        print("2CAPTCHA - grecaptcha v2 site key: '%s' " % site_key)
        print("2CAPTCHA - try to solve, please wait a minute...")

        # captcha_result = {'code': '03AGdBq26r1eGn4Hxza9O4ICb8HfKzdly9POvnIak310R1AUn1rp5Ba68VWZIKyabsLmE6sxsZ0t4iV0PAQkwB60sYPQhMlbDhH0Ldjq1wxOMqIUyw5Hi5z5tSS2i8Fx1nCTZNbk6OJMhwWVkI72Xzj55_8tG4bvLN1hTuiwcGpEIXh3hAw-4Rzk2Klg4f2WRn1gTOcRFxTjCW5MHOBbkrAi2JOgerEdOXT8k_TY0WGmPH8yBx-Z-dSTDY4W43cK84ncJKfuYSbvqGwxYwRMStpO-cutty3JgLpurzaY-rMJpl5DKV18Qv0BXzhlRcrYDd1tFD5shwQnv2MlQBVF7RN7aS974ClDFcfSRbWlQ2d_CYSfIL5WZCeqvqQd3eU_ZHehk4GjNq8zGoxh12XKxxUgq69_Rm10r28em7-sG0eM32Qi5P0cpJ6fBkOK6JzUmSV1XPeomNQbgaMowvxyMHo1yU9k-q9bpCkduOYmK-rDNZFfetPD1CRVV6QH1oAkLTF8kW2TSoNl0Ug2O4lX_fixtgBzO1UAMSm4xvA83nj06j5QPWibiAlbyCDxK5LkUeGuS1MtdJwj49bfameOza890Iz_Y2ZdF9D10OYE7wAjAHostw0ZHRd_uDx1O-GdJn-XLOxolDephTNqhvLHdF14tMyz20c4Rx9arzWvariX3puEg0Y1BdTRJ5_XNXm6xH-v4fEOfraFT8WINvC9frB3ivtbFZgvq5Qq_ZbbfgvEjlC4W-jUkCCz5ou-uh7tC4bL7jd2AH8_Iqv8W0AjFHdM9ZNAcqGkPXLLpP_vciS6PwZcdf83Ix-232h1a7fXqHQcJaksrZaqJTp7_CHe9iQLNv5v-qM36d78UgEECJgu3Wy8BTn_fxC_aQsP4BezOaylQ1vDvBvYmkYwbP6Weutd8bFGD23EpjJCZWZM4_Yj4TF10pxoH1tlU_-XNlDcmyZBuy1VvCkxpxdx-UXJM5HwV_4JpJ73PK1P5Fr3gKGdNDSDgI8aeWPSM-bodzySMbJcPzXScjnF2PqhDcirmE98A1kPEl1PWGBafYLlnkwQdA2dD1RRcPkXGfDQvRzakpBIOtspmpir9U0E24Ka7fxL-ey_-ZauxGEmAq5oG4AEBURRil7nnw6W1PRA8_6sDH_DgwORszJ0FkqBlajyXTeKnab0PLG-pSGSu2xR1EDaK_uFnowci4a_LYKPa9Ztp0TdiLKy7Q2-LlYK-RvzaJ0tMukxKN0YWPULiZkKfO5R7qWumkASgDbIiTJjSAbC1c3VSu_UjtFkkxFrSZUQwQaqkSD7juL6ksWKNlcnY2JxKeAPXnwm5JR9eDHccijj1BwVWAj0qt08ioJB0gKjWiZNTgMKg41vhXDr_IdCw4QdCMwxRo_GzNC3WgCHJDRGe97CfyEVRlUCUP12HMElAygfRDYsZwImHvtRdxeJiRwKE8SvSnqt160_WUXdVXJ9AFlQXoxZNk_6NCNpsh2sVf2wzM_waa2I6CDv4rEFFnxIRKqW0hG99FlS66LOIkUh3L04MefkAo9YfASOjdAiK5dVEg2fLocwYy-vhFqW0SqEjq9G6T2qgZkGx3YkMV_zeFVDLSpR3mdMPfbKvxgm1WatroK9kOe-iqYw'}

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
        js_script = "iframe = document.getElementsByTagName('iframe')[3]; " + \
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

