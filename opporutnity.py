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
        # driver.get('https://www.skillindiadigital.gov.in/opportunities')
        # print(0)
        # #details = driver.find_elements(By.XPATH,'//*[@id="MainContent"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[6]/app-job-card/a')
        # details = driver.find_element(By.CLASS_NAME,'card')
        # driver.execute_script("window.open('about:blank', 'secondtab');")
        # driver.switch_to.window("secondtab")
        # details.click()
        # time.sleep(3)
        # # contact_person = details.find_element(By.XPATH, "//div[@class='analytic-card-description']").text
        # # print(f"Contact Person: {contact_person}")
        driver.get('https://www.skillindiadigital.gov.in/opportunities')  
        

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-detail')))

        card = driver.find_elements(By.CLASS_NAME, 'card-detail')[5]  
        card.click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'analytic-card-description'))
        )
        print(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'analytic-card-description')))
        contact_person = card.find_element(By.XPATH, '//*[@id="mat-tab-content-7-0"]/div/div/div[2]/div/div[4]/div/div/h3').text
        print(f"Contact Person: {contact_person}")
        print(2)
        mobile_number = card.find_element(By.XPATH, '//*[@id="mat-tab-content-7-0"]/div/div/div[2]/div/div[6]/div/div/h3').text
        print(f"Mobile Number: {mobile_number}")
        print(3)
        email = card.find_element(By.XPATH, '//*[@id="mat-tab-content-7-0"]/div/div/div[2]/div/div[7]/div/div/h3').text
        print(f"Email: {email}")
        
        

        
    except Exception as e:
    # Print the error message
        print(f"An error occurred: {e}")
        driver.quit()

def main():
    scrapper()

if __name__ == '__main__':
    main()
