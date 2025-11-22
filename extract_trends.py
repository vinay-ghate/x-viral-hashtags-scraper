import json
import requests
from bs4 import BeautifulSoup

# Fetch HTML from URL
url = 'https://trends24.in/india/'
print(f"Fetching data from {url}...")

# Add headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an error for bad status codes
html_content = response.text

# Save the HTML for debugging
with open('fetched_page.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
    print("Saved fetched HTML to 'fetched_page.html' for debugging")

print("Data fetched successfully!")

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the first trend list (Timeline view)
trend_list = soup.find('ol', class_='trend-card__list')

if not trend_list:
    print("No trend list found!")
    exit(1)

print("Found trend list from Timeline view")

# Find all list items
items = trend_list.find_all('li')
print(f"Found {len(items)} items in the list")

# List to store extracted data
trends_data = []

# Extract first 5 items
count = 0
for i, item in enumerate(items):
    if count >= 5:
        break
    
    # Find the trend link
    link_tag = item.find('a', class_='trend-link')
    
    if link_tag:
        # In the timeline view, duration is not explicitly shown per item in the same way
        # We'll set it to "N/A" for now as it requires cross-referencing multiple lists
        
        data = {
            'rank': str(i + 1),
            'text': link_tag.text.strip(),
            'link': link_tag.get('href', ''),
            'duration': "N/A" 
        }
        
        trends_data.append(data)
        count += 1
        print(f"Extracted trend #{count}: {data['text']}")

# Convert to JSON
json_output = json.dumps(trends_data, indent=2, ensure_ascii=False)

# Print the JSON output
print(json_output)

# Optionally, save to a JSON file
with open('trends_output.json', 'w', encoding='utf-8') as f:
    f.write(json_output)

print("\n\nData has been saved to 'trends_output.json'")
