import requests
from bs4 import BeautifulSoup

# Define the URL of the website you want to crawl
url = "https://meta.vn/huong-dan/tong-hop/vinmart-ha-noi-10325"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the <ul> elements on the page
    ul_elements = soup.find_all('ul')
    
    # Create and open a text file for writing
    with open('extracted_data_winmart2.txt', 'w', encoding='utf-8') as file:
        # Iterate through each <ul> element and find the first <li> element within it
        for ul in ul_elements:
            first_li = ul.find('li')
            if first_li:
                file.write(first_li.text.strip() + '\n')
    
    print("Data has been saved to 'extracted_data.txt'.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
