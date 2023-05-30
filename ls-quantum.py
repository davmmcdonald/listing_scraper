import sys
import ssl
import csv
import os
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime

# Check if the required arguments are provided
if len(sys.argv) < 3:
    print('Error: Expected at least two arguments.')
    print("Usage: python3 ls-quantum.py <url> <output.csv>")
    sys.exit(1)

# Function to format a string by removing HTML tags and extra spaces
def format_string(old_str):
    new_str = re.sub('<.*?>', '', old_str)  # Remove HTML tags
    new_str = ' '.join(new_str.split()).replace('\t', '').replace('\n', ',')  # Remove extra spaces, tabs, and newlines
    new_str = new_str.replace('&amp;', '&').replace('‚Äì', '-') # Replaces some incorrectly displayed characters
    return new_str

# Function to split an address into street and city/state/zip parts
def split_address(address):
    parts = address.split('<br/>')
    street = format_string(parts[0])
    city_state_zip = format_string(parts[1])
    return street, city_state_zip

# Disable SSL certificate verification
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

args = sys.argv
url = args[1]  # URL to scrape data from
csv_filename = args[2]  # Name of the output CSV file
current_directory = os.getcwd()
current_date = datetime.now().date().strftime("%Y-%m-%d")
output_folder = "output/quantum"

# Adds .csv extension to file, if not specified by user
if '.csv' not in csv_filename: 
    csv_filename = csv_filename + '.csv'
    
csv_path = os.path.join(current_directory, output_folder, current_date, csv_filename)

# Open the URL and read the HTML content
page = urlopen(url, context=context)
html = page.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Find relevant elements using their classes
addresses = soup.find_all(class_='property-address')
titles = soup.find_all(class_='property-details-title')
flyers = soup.find_all(lambda tag: tag.name == 'a' and tag.get_text() == 'Download Brochure')

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

# Open the CSV file and write header row
with open(csv_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Address', 'City, State, Zip', 'Listing Title', 'Flyer URL'])
    
    # Iterate over the scraped data and write rows to the CSV file
    for i in range(len(addresses)):
        address, city_state_zip = split_address(addresses[i].prettify().strip())
        title = format_string(titles[i].get_text().strip())
        flyer_url = flyers[i]['href']

        writer.writerow([address, city_state_zip, title, flyer_url])

# Print the number of listings scraped and the path of the CSV file
print(len(addresses), 'listings scraped!')
print('Data saved to', csv_path)