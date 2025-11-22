import requests
from bs4 import BeautifulSoup
from app.models import TrendItem

def fetch_trends(country: str) -> list[TrendItem]:
    """
    Fetches trending topics from trends24.in for a specific country.
    """
    url = f'https://trends24.in/{country}/'
    print(f"Fetching data from {url}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first trend list (Timeline view)
    trend_list = soup.find('ol', class_='trend-card__list')

    if not trend_list:
        print("No trend list found!")
        return []

    items = trend_list.find_all('li')
    trends_data = []

    for i, item in enumerate(items):
        # Find the trend link
        link_tag = item.find('a', class_='trend-link')
        
        if link_tag:
            trend = TrendItem(
                rank=str(i + 1),
                text=link_tag.text.strip(),
                link=link_tag.get('href', ''),
                duration="N/A" 
            )
            trends_data.append(trend)

    return trends_data
