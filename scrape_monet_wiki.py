import requests
from bs4 import BeautifulSoup
import os
from time import sleep
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Define a user agent for your requests
headers = {
    'User-Agent': 'My User Agent 1.0'  # You can customize this user agent
}

def find_original_file_url(image_page_url):
    # Send a GET request to the image page with the user agent header
    image_page = requests.get(image_page_url, headers=headers)
    image_page_soup = BeautifulSoup(image_page.content, "html.parser")
    
    # Find the link with the text "Original File"
    original_file_link = image_page_soup.find("a", string="Original file", href=True)
    if original_file_link:
        original_file_url = original_file_link["href"]
        return original_file_url
    else:
        # If "Original File" link is missing, look for the fullImageLink
        full_image_div = image_page_soup.find("div", {"class": "fullImageLink"})
        if full_image_div:
            full_image_link = full_image_div.find("a", href=True)
            if full_image_link:
                full_image_url = full_image_link["href"]
                return full_image_url
    return None

# Define the URL to scrape
url = "https://www.wikidata.org/wiki/Wikidata:WikiProject_sum_of_all_paintings/Creator/Claude_Monet"

# Send a GET request to the URL and parse the HTML content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table with the desired structure
table = soup.find("table", {"class": "wikitable"})

# Create a directory to save the original files
if not os.path.exists("1.original_files"):
    os.mkdir("1.original_files")

# Get a list of existing files in the folder
existing_files = os.listdir("1.original_files")

# Initialize counters
url_counter = 0
missing_url_counter = 0
skipped_counter = 0

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
                
                # Check if the file already exists in the folder
                if filename in existing_files:
                    print(Fore.YELLOW + f"Skipped: {filename} (already exists)")
                    print(original_file_url)
                    print()
                    skipped_counter += 1
                else:
                    # Download the image
                    image_data = requests.get(original_file_url, headers=headers).content
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_data)
                    print(Fore.GREEN + f"Downloaded: {filename}")
                    print(original_file_url)
                    print()
                    url_counter += 1
                # Add a short delay (1 seconds) before the next download
                sleep(1)
            else:
                missing_url_counter += 1
                print(Fore.RED + f"No high-resolution image found at {image_page_url}")
                print()
    
print(Fore.CYAN + f"Scraped {url_counter} URLs and downloaded the images.")
print(Fore.YELLOW + f"Skipped {skipped_counter} URLs (already exist).")
print(Fore.RED + f"Could not find {missing_url_counter} URLs.")
