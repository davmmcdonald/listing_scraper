# Real Estate Listing Scraper

This is a web scraping script written in Python that extracts data from a website and saves it to a CSV file. It is currently designed to scrape property listings from the following brokerages, with additional sites being added. :sunglasses:

- Hoff & Leigh Commercial Real Estate (ls-hoff-leigh.py)
- Quamtum Commercial Group (ls-quantum.py)
- Kratt Commercial Properties (ls-kratt-commercial.py)

## Usage

Make sure you have Python 3 installed on your system. The script requires the following command-line arguments:

`python3 <script>.py <url> <output>.csv`

- `<url>`: The URL of the web page to scrape data from.
- `<output.csv>`: The name of the output CSV file to save the scraped data.

Before running the script, ensure that you have the necessary packages installed. You can install the required packages by running the following command:

`pip install beautifulsoup4`