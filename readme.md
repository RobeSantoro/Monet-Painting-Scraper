# Monet Painting Scraper

This is a Python script that scrapes a Wikipedia page for image URLs and downloads the corresponding images. The script uses the requests library to send HTTP requests to the Wikipedia page and the BeautifulSoup library to parse the HTML content of the page. The script then iterates through the table rows of the page, extracts image URLs, and downloads the corresponding images using the requests library. The script also logs the progress of the scraping and downloading process to a log file.

Getting Started
To use this script, you will need to have Python 3 installed on your machine. You will also need to install the following Python libraries:

- requests
- beautifulsoup4
- colorama

You can install these libraries using pip. For example:

```bash
pip install requests beautifulsoup4 colorama
```

Usage
To use the script, simply run the scrape_monet_wiki.py file using Python. The script will scrape the Wikipedia page and download the corresponding images to a folder called 1.original_files. The progress of the scraping and downloading process will be logged to a file called download.log.

License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details