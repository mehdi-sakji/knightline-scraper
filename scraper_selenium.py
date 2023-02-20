from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
import pandas as pd
import os
import shutil
import datetime

ts = str(datetime.datetime.now().timestamp())
os.mkdir("resumes-{}".format(ts))

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("download.default_directory="+os.getcwd()+os.path.sep+"resumes")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://ucfbusiness.my.site.com/Knightline/s/login/")

#LOGIN
fill_in_slp = 2
load_slp = 7
print("Login...")
time.sleep(fill_in_slp)
input_email  = driver.find_element(By.CLASS_NAME, "slds-input")
input_email.send_keys("mt@groceryanchored.com")
input_pass = driver.find_elements(By.CLASS_NAME, "slds-input")[1]
input_pass.send_keys("Optics33!")
time.sleep(fill_in_slp)
driver.find_element(By.CLASS_NAME, "slds-button").click()
time.sleep(load_slp)

#GO TO PROFILES PAGE
driver.find_element(By.CLASS_NAME, "emberInnerHeader").find_elements(By.TAG_NAME, "li")[3].click()
time.sleep(load_slp)

#GET NUMBER OF PAGES AND RESUMES IN EACH PAGE --> NBR OF PAGINATION LOOPS
print("Get number of pages and bloc per page...")
banner = driver.find_elements(By.CLASS_NAME, "slds-clearfix")[-1]
tot_resumes = banner.find_element(By.TAG_NAME, "p").text.split(" ")[-1]
tot_resumes = int(tot_resumes)
len_blocs = banner.find_element(By.TAG_NAME, "p").text.split(" ")[2]
len_blocs = int(len_blocs)
n_pages = tot_resumes
# n_pages = 3 # for test

pagination_slp = 2

#SCRAPE PAGES
resumes = []
for page in range(n_pages):
    print("Scraping page ... {}".format(str(page+1)))
    
    if page>=1:
        try:
            driver.find_element(By.CLASS_NAME, "btnBlack").click()
        except:
            driver.get("https://ucfbusiness.my.site.com/Knightline/s/resume-book")
            time.sleep(load_slp)
            for i in range(page):
                driver.find_elements(By.CLASS_NAME, "slds-clearfix")[-1].find_elements(By.TAG_NAME, "button")[-1].click()
                time.sleep(pagination_slp)
        time.sleep(pagination_slp)
        banner = driver.find_elements(By.CLASS_NAME, "slds-clearfix")[-1]
        banner.find_elements(By.TAG_NAME, "button")[-1].click()
        time.sleep(pagination_slp)


    #SCRAPE PROFILES WITHIN PAGE
    blocs = driver.find_elements(By.CLASS_NAME, "slds-size_10-of-12")
    len_blocs = len(blocs)
    # len_blocs = 2 # for test

    for index in range(len_blocs):
        try:
            print("Scraping bloc {} of page {}...".format(str(index+1), str(page+1)))
            if index >= 1:
                try:
                    driver.find_element(By.CLASS_NAME, "btnBlack").click()
                except:
                    driver.get("https://ucfbusiness.my.site.com/Knightline/s/resume-book")
                    time.sleep(load_slp)
                    for i in range(page):
                        driver.find_elements(By.CLASS_NAME, "slds-clearfix")[-1].find_elements(By.TAG_NAME, "button")[-1].click()
                        time.sleep(pagination_slp)

            time.sleep(pagination_slp)
            bloc = driver.find_elements(By.CLASS_NAME, "slds-size_10-of-12")[index]
            bloc.find_element(By.TAG_NAME, "button").click()
            time.sleep(pagination_slp)
            resume = {}

            heading = driver.find_element(By.ID, "Heading")
            resume["Full Name"] = heading.find_elements(By.CLASS_NAME, "sectionHead")[1].text

            print("Scraping {}...".format(resume["Full Name"]))

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
            try:
                print("downloading resume...")
                resume["Resume"] = documents.find_elements(By.TAG_NAME, "a")[-1].text
                documents.find_elements(By.TAG_NAME, "a")[-1].click()
                time.sleep(pagination_slp)
                driver.find_elements(By.CLASS_NAME, "uiButton")[0].click()
                time.sleep(pagination_slp)
                driver.find_elements(By.CLASS_NAME, "uiButton")[2].click()
                time.sleep(pagination_slp*2)
                try:
                    shutil.move(resume["Resume"]+".pdf", "./resumes-{}".format(ts))
                except:
                    try:
                        shutil.move(resume["Resume"]+".docx", "./resumes-{}".format(ts))
                    except:
                        shutil.move(resume["Resume"]+".doc", "./resumes-{}".format(ts))
            except:
                print("No resume for {}".format(resume["Full Name"]))
            resumes.append(resume)
        except:
            print("Couldn't scrape page {} bloc {}".format(str(page), str(index)))
            pass

df_resumes = pd.DataFrame(resumes)
print("Number of scraped profiles: {}".format(str(len(resumes))))
print("Dumping data...")
df_resumes.to_csv("output-{}.csv".format(ts), index=False)
print("Zipping resumes...")
shutil.make_archive('resumes-{}'.format(ts), 'zip', './resumes-{}'.format(ts))
driver.close()
