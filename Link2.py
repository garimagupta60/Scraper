"""
Note : it only extract link of 1st card after it 
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
driver = webdriver.Chrome()

driver.get('https://www.skillindiadigital.gov.in/opportunities')  # Wait until the element is present
wait = WebDriverWait(driver, 10)
cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-job-card:nth-of-type(1) a[tabindex='0']")))



cards = driver.find_elements(By.CSS_SELECTOR, "app-job-card:nth-of-type(1) a[tabindex='0']")
print(type(cards))
links=[]
print(len(cards))
for index, card in enumerate(cards):
    card.click()
    time.sleep(3)  
    link = driver.current_url
    links.append(link)
    
    print(f"Link {index + 1}: {link}")
    driver.back()
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-job-card a[tabindex='0']")))
    cards = driver.find_elements(By.CSS_SELECTOR, "app-job-card a[tabindex='0']")

driver.quit()
