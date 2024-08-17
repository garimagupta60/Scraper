from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import streamlit as st

chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrapper():
    try:
        driver.get('https://www.investindia.gov.in/indian-unicorn-landscape')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "uni-logos")))

        # Select the div with id and class 'uni-logos'
        container = driver.find_element(By.ID, "uni-logos")
        items = container.find_elements(By.TAG_NAME, "a")  # Find all 'a' tags within the container

        results = []
        for item in items:
            data = {}
            try:
                data['website'] = item.get_attribute('href')
                results.append(data)
            except Exception as e:
                print(f"An error occurred: {e}")

        df = pd.DataFrame(results)
        df.to_csv('unicorn.csv', index=False)
        print('Scraping completed. Data saved to unicorn.csv')
    finally:
        driver.quit()

def main():
    scrapper()
    # Uncomment the following lines if you want to integrate with Streamlit
    # st.title("Unicorn Scrapper")
    # if st.button("Scrape Data"):
    #     scrapper()
    #     st.success("File Downloaded Successfully")

if __name__ == '__main__':
    main()
