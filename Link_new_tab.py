# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # Initialize WebDriver
# driver = webdriver.Chrome()

# # Open the website
# driver.get('https://www.skillindiadigital.gov.in/opportunities')

# # Wait for the cards to be present
# wait = WebDriverWait(driver, 10)
# cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-job-card a[tabindex='0']")))

# print(f"Total number of cards found: {len(cards)}")

# for index, card in enumerate(cards):
#     # Open a new tab
#     driver.execute_script("window.open('');")
    
#     # Switch to the new tab
#     driver.switch_to.window(driver.window_handles[1])
#     try:
#         wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='d-flex analytic-card']//h3")))
#         # Extract the URL or any other information needed
#         new_url = driver.current_url
#         print(f"Link {index + 1}: {new_url}")
        
#         # Extract contact details or other required information
#         try:
#             contact_info = driver.find_element(By.CLASS_NAME, 'contact-details').text
#             print(f"Contact Information for Card {index + 1}: {contact_info}")
#         except Exception as e:
#             print(f"Could not find contact information for Card {index + 1}: {e}")
#     except Exception as e:
#         print(f"Page did not load properly for Card {index + 1}: {e}")
    
#     # Close the new tab
#     driver.close()

#     # Switch back to the original tab
#     driver.switch_to.window(driver.window_handles[0])

#     # Wait for the cards to be present again before proceeding
#     cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-job-card a[tabindex='0']")))

# # Quit the driver
# driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the website

index_ = 0

while True:

    driver.get('https://www.skillindiadigital.gov.in/opportunities')

    # Wait for the cards to be present
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    wait = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)
    my_element_id = 'something123'
    
    cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-job-card a[tabindex='0']")))

    print(f"Total number of cards found: {len(cards)}")

    for index, card in enumerate(cards):
        # Click the card to open it in a new tab
        # driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[1])
        if index_+1 == index:
            time.sleep(3)
            try:
                # Click the card element to open its details
                card.click()
                
                # Wait for the new tab to load
                time.sleep(3)
                #wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='d-flex analytic-card']//h3")))
                
                # Extract the URL of the new tab
                new_url = driver.current_url
                print(f"Link {index + 1}: {new_url}")
                index_ = index
                break
            except Exception as e:
                print(f"Page did not load properly for Card {index + 1}: {e}")
    if index_ == 20:
        break
    

    # Close the new tab
    # driver.close()

    # # Switch back to the original tab
    # driver.switch_to.window(driver.window_handles[0])

    # Wait for the cards to be present again before proceeding
    cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-job-card a[tabindex='0']")))

# Quit the driver
driver.quit()
