import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_about_us_page(base_url):
    
    # Make a request to the base URL
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {base_url}: {e}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Search for links that likely point to the 'About Us' page
    keywords = ['about', 'about-us', 'aboutus', 'who-we-are', 'company']
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        for keyword in keywords:
            if keyword in href.lower():
                # Construct the full URL
                about_us_url = urljoin(base_url, href)
                return about_us_url

    # If no link is found that matches the keywords
    print("Could not find an 'About Us' page.")
    return None

def main():
    website = "https://globalittrainings.in/"  # Replace with the target website
    about_us_url = get_about_us_page(website)
    
    if about_us_url:
        print(f"Found 'About Us' page: {about_us_url}")
    else:
        print("No 'About Us' page found.")

if __name__ == "__main__":
    main()
