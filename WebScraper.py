import requests
import csv
from bs4 import BeautifulSoup

# Define facts as variables that will serve as our knowledge base.
url = "https://mcm.edu.ph/programs/college/alfonso-t-yuchengco-college-of-business/accountancy/"
selectors = [
    "#content",
    ".elementor-widget-container",
    ".elementor-widget-wrap elementor-element-populated",
    ".sina-title-title"
]

# Retrieve and parse the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Logic rule for checking if content is unique
def is_unique(content, seen):
    """Rule: Return True if content has not been seen before."""
    return content not in seen

# Logic rule for extracting content based on selectors and tags
def extract_content(selector, tags, seen):
    """Rule: Extract text from specified tags within the given selector."""
    div_element = soup.select_one(selector)
    extracted = []

    if div_element:
        for tag in div_element.find_all(tags):
            content = tag.get_text(strip=True)
            # If it’s an <a> tag, retrieve the link as well
            if tag.name == 'a':
                link = tag.get('href', 'No link found')
                content = f"Text: {content}, Link: {link}"
            if is_unique(content, seen):
                seen.add(content)
                extracted.append((tag.name, content))
    return extracted

# Open CSV file to save extracted content
with open('scraped_accountancy.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Tag", "Content"])
    seen_content = set()

    # Apply rules to each selector
    for selector in selectors:
        extracted_data = extract_content(selector, ['p', 'a', 'li', 'tr', 'h2'], seen_content)
        for tag, content in extracted_data:
            writer.writerow([tag, content])

print("Data saved to scraped_accountancy.csv.")
