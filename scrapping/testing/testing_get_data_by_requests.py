import requests
from bs4 import BeautifulSoup
# URL of the page you want to scrape
page_link = 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/buckets-mugs/?nc=nb&page=5'

# Headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Create a session
session = requests.Session()

# Send the GET request
response = session.get(page_link, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful")
    # Proceed with parsing the response content
    page_content = response.text
    # print(page_content)

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')

    # Now you can use BeautifulSoup to extract the desired data
    print(soup.prettify())
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)