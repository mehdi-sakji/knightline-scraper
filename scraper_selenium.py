from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://ucfbusiness.my.site.com/Knightline/s/login/")

#LOGIN
time.sleep(3)
input_email  = driver.find_element(By.CLASS_NAME, "slds-input")
input_email.send_keys("mt@groceryanchored.com")
input_pass = driver.find_elements(By.CLASS_NAME, "slds-input")[1]
input_pass.send_keys("Optics33!")
time.sleep(1)
driver.find_element(By.CLASS_NAME, "slds-button").click()
time.sleep(6)

#GO TO PROFILES PAGE
driver.find_element(By.CLASS_NAME, "emberInnerHeader").find_elements(By.TAG_NAME, "li")[3].click()
time.sleep(3)

#SCRAPE PROFILES
blocs = driver.find_elements(By.CLASS_NAME, "slds-size_10-of-12")
len_blocs = len(blocs)
len_blocs = 1

resumes = []

for index in range(len_blocs):
    bloc = driver.find_elements(By.CLASS_NAME, "slds-size_10-of-12")[index]
    bloc.find_element(By.TAG_NAME, "button").click()
    time.sleep(3)
    resume = {}
    
    heading = driver.find_element(By.ID, "Heading")
    resume["Full Name"] = heading.find_elements(By.CLASS_NAME, "sectionHead")[1].text
    resume["First Name"] = resume["Full Name"].split(" ")[0]
    resume["Email"] = heading.find_element(By.TAG_NAME, "a").get_attribute('href').replace("mailto:", "")
    resume["Phone Number"] = heading.find_elements(By.TAG_NAME, "a")[1].get_attribute('href').replace("tel:", "")

    main_content = driver.find_element(By.CLASS_NAME, "slds-wrap")

    overview = main_content.find_elements(By.CLASS_NAME, "slds-col")[-2]
    paragraphs_overview = overview.find_elements(By.CLASS_NAME, "sectionText")
    resume["Major"] = paragraphs_overview[1].text
    resume["Minor"] = paragraphs_overview[3].text
    resume["GPA"] = paragraphs_overview[5].text
    resume["Class Standing"] = paragraphs_overview[7].text
    resume["Graduation Date"] = paragraphs_overview[9].text

    details = main_content.find_elements(By.CLASS_NAME, "slds-col")[0]
    resume["Desired Industry"] = details.find_elements(By.CLASS_NAME, "slds-col")[-1].find_elements(By.TAG_NAME, "p")[1].text
    resume["Desired Positions"] = details.find_elements(By.CLASS_NAME, "slds-col")[1].find_elements(By.TAG_NAME, "p")[1].text

    documents = driver.find_elements(By.CLASS_NAME, "slds-wrap")[-1]
    resume["Resume"] = documents.find_elements(By.TAG_NAME, "a")[-1].text
    resumes.append(resume)

print(resumes)
driver.close()
