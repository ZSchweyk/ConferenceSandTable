from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys

sys.path.append("/usr/lib/chromium-browser/chromedriver")

def find_period(equation: str):
    options = Options()
    options.headless = False
    # options.binary_location = ""

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    browser.get("https://www.desmos.com/calculator")



find_period("3*sin(4*theta)")


