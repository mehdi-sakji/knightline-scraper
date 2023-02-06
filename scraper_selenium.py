from selenium import webdriver

CHROMEDRIVER_PATH = './chromedriver.exe'

browser = webdriver.Chrome(CHROMEDRIVER_PATH)
browser.get('www.google.com')
