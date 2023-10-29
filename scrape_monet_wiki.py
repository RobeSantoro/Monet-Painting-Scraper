import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

original_file_folder = "1.original_files"

# Define the URL to scrape
url = "https://www.wikidata.org/wiki/Wikidata:WikiProject_sum_of_all_paintings/Creator/Claude_Monet"

# Define a user agent for your requests
headers = {
    'User-Agent': 'My User Agent 1.0'  # You can customize this user agent
}


def find_original_file_url(image_page_url):
    # Send a GET request to the image page with the user agent header
    image_page = requests.get(image_page_url, headers=headers)
    image_page_soup = BeautifulSoup(image_page.content, "html.parser")

    # Find the link with the text "Original File"
    original_file_link = image_page_soup.find(
        "a", string="Original file", href=True)
    if original_file_link:
        original_file_url = original_file_link["href"]
        return original_file_url
    else:
        # If "Original File" link is missing, look for the fullImageLink
        full_image_div = image_page_soup.find(
            "div", {"class": "fullImageLink"})
        if full_image_div:
            full_image_link = full_image_div.find("a", href=True)
            if full_image_link:
                full_image_url = full_image_link["href"]
                return full_image_url
    return None


# Send a GET request to the URL and parse the HTML content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table with the desired structure
table = soup.find("table", {"class": "wikitable"})

# Create a directory to save the original files
if not os.path.exists(original_file_folder):
    os.mkdir(original_file_folder)

# Get a list of existing files in the folder
existing_files = os.listdir(original_file_folder)

# Initialize counters
url_counter = 0
missing_url_counter = 0
skipped_counter = 0
td_counter = 0

# Iterate through the table rows and extract image URLs
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if len(cells) >= 2:

        image_link = cells[0].find("a", href=True)
        label = cells[1].find("a", href=True)

        # Clean the label text
        label = label.text.replace(" ", "_").replace("(", "").replace(")", "").replace(
            "é", "e").replace("è", "e").replace("à", "a").replace("ç", "c").replace(
            "ô", "o").replace("ö", "o").replace("ü", "u").replace("ë", "e").replace(
            "â", "a").replace("î", "i").replace("ê", "e").replace("û", "u").replace(
            "ù", "u").replace("ï", "i").replace("œ", "oe").replace("ÿ", "y").replace(
            "É", "E").replace("È", "E").replace("À", "A").replace("Ç", "C").replace(
            "Ô", "O").replace("Ö", "O").replace("Ü", "U").replace("Ë", "E").replace(
            "Â", "A").replace("Î", "I").replace("Ê", "E").replace("Û", "U").replace(
            "Ù", "U").replace("Ï", "I").replace("Œ", "OE").replace("Ÿ", "Y").replace(
            "’", "").replace(":", "").replace("!", "").replace("?", "").replace(
            '"', "").replace(
            "'", "").replace(".", "").replace(",", "").replace(";", "").replace(
            "«", "").replace("»", "").replace("–", "").replace("-", "").replace(
            "—", "").replace("–", "").replace("(", "").replace(")", "").replace(
            "“", "").replace("”", "").replace("„", "").replace("…", "").replace(
            "°", "").replace("‘", "").replace("’", "").replace("´", "").replace(
            "¨", "").replace("·", "").replace("†", "").replace("‡", "").replace(
            "‰", "").replace("‹", "").replace("›", "").replace("€", "").replace(
            "$", "").replace("£", "").replace("¥", "").replace("¢", "").replace(
            "¡", "").replace("¿", "").replace("§", "").replace("©", "").replace(
            "®", "").replace("™", "").replace("¶", "").replace("†", "").replace(
            "‡", "").replace("°", "").replace("•", "").replace("·", "").replace(
            "…", "").replace("′", "").replace("″", "").replace("‹", "").replace(
            "›", "").replace("§", "").replace("№", "").replace("÷", "").replace(
            "×", "").replace("±", "").replace("∞", "").replace("≠", "").replace(
            "≤", "").replace("≥", "").replace("µ", "").replace("∂", "").replace(
            "∑", "").replace("∏", "").replace("π", "").replace("∫", "").replace(
            "ª", "").replace("º", "").replace("Ω", "").replace("æ", "").replace(
            "ø", "").replace("¿", "").replace("¡", "").replace("¬", "").replace(
            "√", "").replace("ƒ", "").replace("≈", "").replace("∆", "").replace(
            "«", "").replace("»", "").replace("…", "").replace("≠", "")

        if image_link:
            image_page_url = "https://commons.wikimedia.org" + \
                image_link["href"]

            original_file_url = find_original_file_url(image_page_url)
            if original_file_url:

                # Extract the filename from the URL
                # filename = original_file_url.split("/")[-1]

                extension = image_link["href"].split(".")[-1]
                filename = label + "." + extension

                extension = original_file_url.split(".")[-1]
                image_path = os.path.join(original_file_folder, filename)

                # Check if the file already exists in the folder
                if filename in existing_files:
                    print(Fore.YELLOW +
                          f"Exists: {filename}")
                    print(original_file_url)
                    print()
                    skipped_counter += 1
                else:
                    # Download the image
                    image_data = requests.get(
                        original_file_url, headers=headers).content
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_data)
                    print(Fore.GREEN + f"Downloaded: {filename}")
                    print(original_file_url)
                    print()
                    url_counter += 1
                # Add a short delay (0.1 seconds) before the next download
                sleep(0.1)
            else:
                missing_url_counter += 1
                print(Fore.RED + f"No high-res found at {image_page_url}")
                print()
        else:
            print(Fore.RED + "No image link found.")
            print()
    td_counter += 1

print(Fore.CYAN + f"Scraped {url_counter} URLs and downloaded the images.")
print(Fore.YELLOW + f"Skipped {skipped_counter} URLs (already exist).")
print(Fore.RED + f"Could not find {missing_url_counter} URLs.")
print(Fore.BLUE + f"Total number of table cells: {td_counter}")
