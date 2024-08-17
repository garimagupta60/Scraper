"""
Note : This Script is working properly, extarcting all requrired details from Given link

Pending Task: To extarct Diffrent links from cards
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get('https://www.skillindiadigital.gov.in/job/detail/0b47a6e9-d98c-454f-ae44-6b565af0f510')

wait = WebDriverWait(driver, 10)
function_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='d-flex analytic-card']//h3")))
function = function_element.text
name_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mat-tab-content-0-0"]/div/div/div[2]/div/div[4]/div/div/h3')))
name = name_element.text
phone_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'tel')]")))
phone_number = phone_element.text
email_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mat-tab-content-0-0"]/div/div/div[2]/div/div[7]/div/div/h3/a')))
email_element = email_element.text
print("Functional Area:", function)
print("Contact Person Name:", name)
print("Mobile Number:", phone_number)
print("Email:", email_element)
driver.quit()
