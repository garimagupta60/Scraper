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

chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

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
        print(1)
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
    print(data)

def scraper(website):
        try: 
            print("*********ABOUT*********************************************************************************************")
            about_us_url =  get_about_us_page(website)
            if about_us_url:
                print(f"Found 'About Us' page: {about_us_url}")
                #search_query = website +  about_us_url
                scrap_data(about_us_url)
            else:
                print("No 'About Us' page found.")
            
            print("*********course***************************************************************************************************")
            course_url = get_courses_page(website)
            if course_url:
                search_query = website +  course_url
                scrap_data(course_url)
            else:
                print("No 'Course' page found.")

            print("*********service*************************************************************************************************")
            service_url = get_service_page(website)
            if service_url:
                search_query = website +  service_url
                scrap_data(service_url)
            else:
                print("No 'Course' page found.")

        finally:
            driver.quit()

def main():
    query = "https://globalittrainings.in/"
    query = "https://www.inventateq.com/"
    #query = "https://seldomindia.com/"
    scraper(query)                                   

if __name__ == '__main__':
    main()
