from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import streamlit as st
import time
options = webdriver.ChromeOptions()
options.add_argument('headless')
chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrapper():
    try:
        result =[]
        for year in range(2010,2025):
                try:
                    driver.get(f'https://www.chittorgarh.com/report/ipo-in-india-list-main-board-sme/82/?year={year}')
                    skip_button = driver.find_element(By.ID,'splashBackURL')
                    skip_button.click()
                except:
                     pass    

                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table-responsive')))

                rows = driver.find_elements(By.XPATH, "//table[@class='table table-bordered table-striped table-hover w-auto']//tbody//tr")
                #print(len(rows))
                
                for i in range(0,len(rows)):
                    data={}
                    container = driver.find_elements(By.XPATH,f'//*[@id="report_data"]/div/table/tbody/tr[{i}]/td[1]/a')
                    for j in container:
                        ipo_name = j.text
                        print(i,ipo_name)
                        company_name = ipo_name[:-3]
                        data['company_name']= company_name

                        words = company_name.split()
                        query_string = '+'.join(words)

                        driver.execute_script("window.open('about:blank', 'secondtab');")
                        driver.switch_to.window("secondtab")
                        driver.get(f"https://www.google.com/search?q={query_string}")
                        time.sleep(2)
                        #google_search_url = f"https://www.google.com/search?q={query_string}"
                        texts = driver.find_elements(By.XPATH, "//*[@role='text']")
                        for text in texts:
                            data['website'] = text.text
                            #print(text.text)
                            break
                        result.append(data)
                        driver.close()
                        #time.sleep(5)
                        driver.switch_to.window(driver.window_handles[0])
        df = pd.DataFrame(result)
        df.to_csv(f'ipo_.csv', index=False)
    except Exception as e:
         print("Error Occur as",e)
         driver.quit()
def main():
    scrapper()

if __name__ == '__main__':
    main()
