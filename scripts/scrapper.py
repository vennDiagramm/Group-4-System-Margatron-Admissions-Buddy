import requests
import csv
from bs4 import BeautifulSoup

# URL to scrape
url = "https://mcm.edu.ph/programs/college/college-of-arts-and-science/bachelor-of-science-in-physical-therapy/"

# Make a request to get the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Open a CSV file to store the scraped data
with open('scrapped_PT.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write headers
    writer.writerow(["Tag", "Content"])

    # Set to track unique content
    seen_content = set()

    # Updated div selectors to scrape
    divs_to_scrape = [
        "#main > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-992cf69",
        "#post-41940 > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-1d06d2c.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div",
        "#post-41940 > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-c6eba09.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div",
        "#post-41940 > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-6a06a3a.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div"
    ]

    # Loop through each selector and extract relevant tags
    for div_selector in divs_to_scrape:
        div_element = soup.select_one(div_selector)

        if div_element:
            # Scrape <p>, <ul>, <li>, and <a> tags, and headers
            for tag in div_element.find_all(['p', 'ul', 'li', 'a', 'h1', 'h2', 'h3', 'h4']):
                tag_name = tag.name
                # Extract the text content from the tag
                text_content = tag.get_text(strip=True)

                # If it's an <a> tag, also extract the href attribute (URL)
                if tag_name == 'a':
                    link = tag.get('href', 'No link found')
                    text_content = f"Text: {text_content}, Link: {link}"

                # Only write non-empty and unique text
                if text_content and text_content not in seen_content:
                    seen_content.add(text_content)  # Add content to the set
                    writer.writerow([tag_name, text_content])

print("Data saved to scrapped_PT.csv.")
