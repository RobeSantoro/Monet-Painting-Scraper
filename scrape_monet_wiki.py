import requests
from bs4 import BeautifulSoup
import os

def find_original_file_url(image_page_url):
    # Send a GET request to the image page and parse the HTML
    image_page = requests.get(image_page_url)
    image_page_soup = BeautifulSoup(image_page.content, "html.parser")
    
    # Find the link with the text "Original File"
    original_file_link = image_page_soup.find("a", text="Original file", href=True)
    if original_file_link:
        original_file_url = original_file_link["href"]
        return original_file_url
    else:
        return None

# Define the URL to scrape
url = "https://www.wikidata.org/wiki/Wikidata:WikiProject_sum_of_all_paintings/Creator/Claude_Monet"

# Send a GET request to the URL and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table with the desired structure
table = soup.find("table", {"class": "wikitable"})

# Create a directory to save the original files
if not os.path.exists("1.original_files"):
    os.mkdir("1.original_files")

# Initialize a counter to count the scraped URLs
url_counter = 0
missing_url_counter = 0

# Iterate through the table rows and extract image URLs
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if len(cells) >= 2:
        image_link = cells[0].find("a", href=True)
        if image_link:
            image_page_url = "https://commons.wikimedia.org" + image_link["href"]
            
            original_file_url = find_original_file_url(image_page_url)
            if original_file_url:
                # Extract the filename from the URL
                filename = original_file_url.split("/")[-1]
                image_path = os.path.join("1.original_files", filename)
                
                # Download the "Original File" image
                image_data = requests.get(original_file_url).content
                with open(image_path, "wb") as img_file:
                    img_file.write(image_data)
                    print(f"Downloaded: {filename}")
                url_counter += 1
            else:
                missing_url_counter += 1
                print(f"Original File URL not found at {image_page_url}")

print(f"Scraped {url_counter} URLs and downloaded the images.")
print(f"Could not find {missing_url_counter} URLs.")
