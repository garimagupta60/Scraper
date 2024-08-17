# https://www.skillindiadigital.gov.in/job/detail/5babb11d-00dd-4f21-8bce-77ed97723f0a
# //*[@id="MainContent"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[6]/app-job-card/a   
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

def scrapper():
    try:
        driver.get('https://www.skillindiadigital.gov.in/opportunities')  

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-detail')))
        
        job_cards = driver.find_elements(By.XPATH, "//app-job-card//a")
        no_of_cards = len(job_cards)
        for i in range(no_of_cards):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-detail')))
            job_cards = driver.find_elements(By.CLASS_NAME, 'card-detail')[i+1]  
            job_cards.click()
            #print(driver.current_url)
            # driver.execute_script("window.open('');")
            # driver.switch_to.window(driver.window_handles[1])
            new_website = driver.current_url
            print(new_website)
            driver.back()

        #     #time.sleep(3)

        

        
        # driver.get('https://www.skillindiadigital.gov.in/job/detail/5babb11d-00dd-4f21-8bce-77ed97723f0a')
        # wait = WebDriverWait(driver, 10)
        # function_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='d-flex analytic-card']//h3")))
        # function = function_element.text
        # name_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mat-tab-content-0-0"]/div/div/div[2]/div/div[4]/div/div/h3')))
        # name = name_element.text
        # phone_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'tel')]")))
        # phone_number = phone_element.text
        # email_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mat-tab-content-0-0"]/div/div/div[2]/div/div[7]/div/div/h3/a')))
        # email_element = email_element.text
        # print("Functional Area:", function)
        # print("Contact Person Name:", name)
        # print("Mobile Number:", phone_number)
        # print("Email:", email_element)
        
        

        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()

def main():
    scrapper()

if __name__ == '__main__':
    main()
