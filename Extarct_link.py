from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import streamlit as st
import time

chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome() 
driver.maximize_window()

driver.get('https://www.skillindiadigital.gov.in/opportunities')  

job_urls = []

while True:
    job_cards = driver.find_elements(By.XPATH, "//app-job-card//a[@tabindex='0']")
    for i in range(len(job_cards)):
        try:
            job_cards = driver.find_elements(By.CLASS_NAME, "card")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "card")))
            job_cards[i].click()
            time.sleep(2) 
            
            job_url = driver.current_url
            job_urls.append(job_url)
            if(i==10):
                break 
            
        except Exception as e:
            print(f"Error occurred: {e}")
            continue
    
    try:
        next_button = driver.find_element(By.CLASS_NAME, "pagination-next") 
        if next_button.is_enabled():
            next_button.click()
            time.sleep(3)
        else:
            break
    except:
        break

for url in job_urls:
    print(url) 


driver.quit()