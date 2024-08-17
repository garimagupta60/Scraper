from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import Details

chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
cities = [
    "Bengaluru", "Chennai", "Hyderabad", "Mumbai", "Pune", "Delhi",
    "Kanpur", "Varanasi", "Kharagpur", "Roorkee", "Guwahati", "Kolkata",
    "Ahmedabad", "Indore", "Patna", "Bhubaneswar", "Tiruchirappalli",
    "Jodhpur", "Jaipur", "Surat", "Coimbatore", "Visakhapatnam", "Nagpur",
    "Mysuru", "Lucknow", "Noida", "Aligarh", "Ranchi", "Amritsar",
    "Chandigarh", "Kozhikode", "Bhopal", "Gandhinagar", "Dehradun",
    "Warangal", "Dhanbad", "Kochi", "Vadodara", "Raipur", "Trivandrum",
    "Gwalior", "Jabalpur", "Agra", "Meerut", "Udaipur", "Mangalore",
    "Vellore", "Thrissur", "Allahabad", "Puducherry"
]
cities1 = [
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Chennai",
    "Gurgaon",
    "Noida",
    "Mumbai",
    "Delhi",
    "Ahmedabad",
    "Kolkata",
    "Jaipur",
    "Indore",
    "Nagpur",
    "Surat",
    "Bhubaneswar",
    "Coimbatore",
    "Lucknow",
    "Vishakhapatnam",
    "Mysuru",
    "Kochi"
]



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


def get_courses_page(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {base_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    keywords = ['courses', 'course-us', 'all-courses', 'our-courses', 'catalog']
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        for keyword in keywords:
            if keyword in href.lower():
                about_us_url = urljoin(base_url, href)
                return about_us_url

    print("Could not find an 'Courses' page.")
    return None


def get_service_page(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {base_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    keywords = ['service', 'services', 'all-service', 'our-service', 'programs']
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        for keyword in keywords:
            if keyword in href.lower():
                about_us_url = urljoin(base_url, href)
                return about_us_url

    print("Could not find an 'Service' page.")
    return None


def scrap_data(website):
    driver.get(f'{website}')
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable().click())
    except Exception:
        pass
    data = driver.find_element(By.TAG_NAME,'body').text
    return data



def scraper(query):
    try: 
        keyword = query 
        driver.get(f'https://www.google.com/maps/search/{keyword}/')
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
        except Exception:
            pass
        results = []    
        for i in cities1:
            

            #switch to second tab
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
                                    var scrollHeightAfter = scrollableDiv.scrollHeight;
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
            

            for item in items:
                data = {}

                try:
                    data['title'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
                except Exception:
                    pass

                # try:
                #     text_content = item.text
                #     phone_pattern = r'((\+?\d{1,2}[ -]?)?(\(?\d{3}\)?[ -]?\d{3,4}[ -]?\d{4}|\(?\d{2,3}\)?[ -]?\d{2,3}[ -]?\d{2,3}[ -]?\d{2,3}))'
                #     matches = re.findall(phone_pattern, text_content)
                #     phone_numbers = [match[0] for match in matches]
                #     unique_phone_numbers = list(set(phone_numbers))
                #     data['phone'] = unique_phone_numbers[0] if unique_phone_numbers else None   
                # except Exception:
                #     pass

                # try:
                #     address_pattern = r'(?:\d+\s)?[A-Za-z0-9\s.,-]+,\s[A-Za-z\s]+(?:,\s[A-Z]{2}\s\d{5})?'
                #     matches = re.findall(address_pattern, text_content)
                #     unique_addresses = list(set(matches))
                #     data['address'] = unique_addresses[0] if unique_addresses else None      
                # except Exception:
                #     pass

                try:
                    data['website'] = item.find_element(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction] div > a').get_attribute('href')
                    url = data['website']
                except Exception:
                    pass    

                if data.get('title'):
                    results.append(data)
            driver.close()
                #time.sleep(5)
            driver.switch_to.window(driver.window_handles[0])    
        
            # df = pd.DataFrame(results)
            # df.to_csv(f'{final_query}.csv', index=False)
            # print(f'Scraping completed. Data saved to {final_query}.csv')
        df = pd.DataFrame(results)
        df.to_csv('Training_cenetr.csv', index=False)
        print(f'Scraping completed. Data saved to {final_query}.csv')
    
    finally:
        driver.quit()


def main():
    # st.title("Google Map Scraper")
    # location = st.text_input("Enter Location here", "")
    # query = st.text_input("Enter Query here", "")
    # if st.button("Find"):
    #     scraper(location, query)
    #     st.success("File Downloaded Successfully")
    query = "Top placement training companies"
    scraper(query)

if __name__ == '__main__':
    main()
