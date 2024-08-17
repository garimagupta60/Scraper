from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

cities1 = ["Jaipur"]

def get_about_us_page(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {base_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    keywords = ['about', 'about-us', 'aboutus', 'who-we-are', 'company']
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        for keyword in keywords:
            if keyword in href.lower():
                about_us_url = urljoin(base_url, href)
                return about_us_url

    print("Could not find an 'About Us' page.")
    return None

def extract_about_us_info(website):
    about_us_url = get_about_us_page(website)
    if not about_us_url:
        return None
    
    try:
        response = requests.get(about_us_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve About Us page: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)
    return text_content

def scraper(query):
    try: 
        driver.get(f'https://www.google.com/maps/search/{query}/')
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
        except Exception:
            pass

        for i in cities1:
            # Switch to a new tab
            driver.execute_script("window.open('about:blank', 'secondtab');")
            driver.switch_to.window("secondtab")

            final_query = query + ' in ' + i
            driver.get(f'https://www.google.com/maps/search/{final_query}/')
            scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
            driver.execute_script("""
                var scrollableDiv = arguments[0];
                function scrollWithinElement(scrollableDiv) {
                    return new Promise((resolve, reject) => {
                        var totalHeight = 0;
                        var distance = 1000;
                        var scrollDelay = 3000;
                        
                        var timer = setInterval(() => {
                            var scrollHeightBefore = scrollableDiv.scrollHeight;
                            scrollableDiv.scrollBy(0, distance);
                            totalHeight += distance;

                            if (totalHeight >= scrollHeightBefore) {
                                totalHeight = 0;
                                setTimeout(() => {
                                    var scrollHeightAfter = scrollHeightBefore;
                                    if (scrollHeightAfter > scrollHeightBefore) {
                                        return;
                                    } else {
                                        clearInterval(timer);
                                        resolve();
                                    }
                                }, scrollDelay);
                            }
                        }, 200);
                    });
                }
                return scrollWithinElement(scrollableDiv);
            """, scrollable_div)

            items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')
            results = []

            for item in items:
                data = {}

                try:
                    data['title'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
                except Exception:
                    pass

                try:
                    text_content = item.text
                    phone_pattern = r'((\+?\d{1,2}[ -]?)?(\(?\d{3}\)?[ -]?\d{3,4}[ -]?\d{4}|\(?\d{2,3}\)?[ -]?\d{2,3}[ -]?\d{2,3}[ -]?\d{2,3}))'
                    matches = re.findall(phone_pattern, text_content)
                    phone_numbers = [match[0] for match in matches]
                    unique_phone_numbers = list(set(phone_numbers))
                    data['phone'] = unique_phone_numbers[0] if unique_phone_numbers else None   
                except Exception:
                    pass

                try:
                    address_pattern = r'(?:\d+\s)?[A-Za-z0-9\s.,-]+,\s[A-Za-z\s]+(?:,\s[A-Z]{2}\s\d{5})?'
                    matches = re.findall(address_pattern, text_content)
                    unique_addresses = list(set(matches))
                    data['address'] = unique_addresses[0] if unique_addresses else None      
                except Exception:
                    pass

                try:
                    data['website'] = item.find_element(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction] div > a').get_attribute('href')
                    url = data['website']
                    data['about_us'] = extract_about_us_info(url)  # Extract 'About Us' page info
                except Exception:
                    pass    

                if data.get('title'):
                    results.append(data)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
        
            df = pd.DataFrame(results)
            filename = f'{final_query}.csv'
            df.to_csv(filename, index=False)
            print(f'Scraping completed. Data saved to {filename}')
    
    finally:
        driver.quit()

def main():
    query = "Top placement training companies"
    scraper(query)

if __name__ == '__main__':
    main()
