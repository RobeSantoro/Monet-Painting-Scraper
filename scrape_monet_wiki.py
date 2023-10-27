import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = "https://www.wikidata.org/wiki/Wikidata:WikiProject_sum_of_all_paintings/Creator/Claude_Monet"

# Send a GET request to the URL and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table with the desired structure
table = soup.find("table", {"class": "wikitable"})

# Initialize a counter to count the scraped URLs
url_counter = 0

# Iterate through the table rows and extract image URLs
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if len(cells) >= 2:
        image_link = cells[0].find("a", href=True)
        if image_link:
            image_page_url = "https://commons.wikimedia.org" + image_link["href"]

            # Print the URL instead of downloading it
            print(f"{image_page_url}")
            
            url_counter += 1

print(f"Scraped {url_counter} URLs.")
