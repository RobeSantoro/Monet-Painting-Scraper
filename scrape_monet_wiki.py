import requests
from bs4 import BeautifulSoup
import os

# Define the URL to scrape
url = "https://www.wikidata.org/wiki/Wikidata:WikiProject_sum_of_all_paintings/Creator/Claude_Monet"

# Send a GET request to the URL and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table with the desired structure
table = soup.find("table", {"class": "wikitable"})

# Create a directory to save the images
if not os.path.exists("Monet_Paintings"):
    os.mkdir("Monet_Paintings")

# Iterate through the table rows and extract image URLs
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if len(cells) >= 2:
        image_link = cells[0].find("a", href=True)
        if image_link:
            image_page_url = "https://commons.wikimedia.org" + image_link["href"]
            
            # Send a GET request to the image page and parse the HTML
            image_page = requests.get(image_page_url)
            image_page_soup = BeautifulSoup(image_page.content, "html.parser")
            
            # Find the high-resolution image link
            image = image_page_soup.find("a", {"class": "internal", "href": True})
            if image:
                high_res_image_url = image["href"]
                
                # Download the high-resolution image
                image_filename = os.path.basename(high_res_image_url)
                image_path = os.path.join("Monet_Paintings", image_filename)
                # image_data = requests.get(high_res_image_url).content
                # with open(image_path, "wb") as img_file:
                #     img_file.write(image_data)
                #     print(f"Downloaded: {image_filename}")
            else:
                print(f"No high-resolution image found for {image_page_url}")
        else:
            print(f"No image link found in row: {row}")
    else:
        print(f"Insufficient data in row: {row}")

print("Download completed.")
