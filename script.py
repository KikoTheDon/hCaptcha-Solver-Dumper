import time
import requests
import re
import json
import os
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import undetected_chromedriver.v2 as uc
 
API_KEY = ""

# This wasn't used though it is very important when submitting hCaptcha requestKeys.
def SetValue(driver, Object, Key, Value):
    driver.execute_script("arguments[0]." + Key + " = '" + Value + "';", Object) 
    
def Open(Url):
    driver = uc.Chrome() # UnDetected Selenium Browser (Very Buggy, a lot of crashes)
    driver.get(Url) # Visit url
    os.system("cls") # Clear Console
    
    # Infinite Loop which breaks if the element has been found.
    # Only prints once using 'didPrint' boolean.
    didPrint = False
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@id="cf-hcaptcha-container"]/iframe')
            print("Captcha has loaded!")
            break
        except NoSuchElementException:
            if not didPrint:
                print("Waiting for hCaptcha to load..")
            didPrint = True
    
    # Container is the form with a lot of the information we want.
    # TextArea is important for submitting the information.
    Container = driver.find_element(By.XPATH, '//*[@id="cf-hcaptcha-container"]/iframe')
    # This would get around tricks that attempt to hide the TextArea.
    TextArea  = driver.find_element_by_id('h-captcha-response-' + Container.get_attribute("data-hcaptcha-widget-id"))

    # Source of form.
    Source    = Container.get_attribute("src")
    SiteKey   = re.search('&sitekey=(.*)', Source).group(1) # Find sitekey using string search.
    print("Dumped site-key ->", SiteKey)

    # Post all information about the Captcha to 2Captcha's servers so that it can be solved.
    CaptchaResponse = requests.get("http://2captcha.com/in.php?key=" + API_KEY + "&sitekey=" + SiteKey + "&method=hcaptcha&pageurl=" + Url).text

    print("Captcha Response ->", CaptchaResponse)
    if CaptchaResponse.find("OK") < 0: # Was the Captcha accepted?
        print("Captcha failed.")
        exit()
    # If you're here then yes, it was accepted.
    captcha_id = CaptchaResponse[3:999] # The Id of the Captcha (2Captcha generated?).
    print("Captcha Id:", captcha_id)

    requestKey = ""
    # Infinite Loop until 2Captcha tells us that it was solved by their workers.
    while True:
        outInfo = requests.get("http://2captcha.com/res.php?key=" + API_KEY + "&json=1&action=get&id=" + captcha_id).json()
        if outInfo["status"] == 0: # If Status is 0 then it hasn't been solved just yet.
            print("Captcha has not been solved, please wait..")
        else: # If it isn't 0 then it has been solved.
            print("Captcha has been solved!")
            requestKey = outInfo["request"] # Cache the key.
            break;
        time.sleep(3)
    if requestKey == "": # Is key empty?
        print("Something went wrong but we don't know what the issue is!")
        exit()

    print("Request Key ->", requestKey) # Output the Captcha key.

# Example Url that was used for testing.
# No other website was tested.
Open("https://smsreceivefree.com/")
