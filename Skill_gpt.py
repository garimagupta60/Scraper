from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert

def scraper():
    driver = webdriver.Chrome()
    driver.get('https://www.skillindiadigital.gov.in/opportunities')

    print(1)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-list')))

    print(2)
    job_cards = driver.find_elements(By.XPATH, "//app-job-card//a[@tabindex='0']")
    no_of_cards = len(job_cards)
    print("Total cards found:", no_of_cards)
    
    for i in range(no_of_cards):
        try:
            print(f"Processing card {i+1}/{no_of_cards}")
            
            # Refresh the list of job cards to avoid stale element reference error
            job_cards = driver.find_elements(By.XPATH, "//app-job-card//a[@tabindex='0']")
            
        except Exception as e:
            print(f"An error occurred while processing card {i+1}: {e}")
            continue

    driver.quit()

# Run the scraper function
scraper()
