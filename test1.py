from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from discord_webhook import DiscordWebhook
import time
#heroku option
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
'''
#self test option
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver-manager

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
cc = ""
def log_in():#login after getting to right site
    driver.get("https://letsgo.golf/los-verdes-golf-course/login")
    #li = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/div/div/div[2]/a[1]"))
    #li.click()
    #WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='email']").send_keys("praiseper02@gmail.com"))
    #WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='password']").send_keys("Pyrian#863" + Keys.ENTER))
    driver.find_element(by = By.XPATH, value = "//*[@id='email']").send_keys("praiseper02@gmail.com")
    driver.find_element(by = By.XPATH, value = "//*[@id='password']").send_keys("Pyrian#863" + Keys.ENTER)
    global cc
    cc = "aasdads"
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/962250301795078184/Wv6ROcglKg9wIf_iylq2uDkwqYDIKabwbocKwPlQMqlnFYyVO8TgiMN2KOowBG3xwZQx', content = 'got')
    #response = webhook.execute()

    
log_in()
#driver.get("https://letsgo.golf/los-verdes-golf-course/login")
print(driver.current_url)
webhook = DiscordWebhook(url='https://discord.com/api/webhooks/962250301795078184/Wv6ROcglKg9wIf_iylq2uDkwqYDIKabwbocKwPlQMqlnFYyVO8TgiMN2KOowBG3xwZQx', content = cc)
response = webhook.execute()
time.sleep(5)
# Now you can start using Selenium