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






    # /pd/40280785/bodyguard-baby-bathing-bar-gently-cleanses-moisturises-no-parabens-75-g/?nc=l3category&t_pos_sec=1&t_pos_item=6&t_s=Moisturizing%2520Baby%2520Bathing%2520Soap%2520Bar%2520for%2520Kids%2520%25E2%2580%2593%2520Pack%2520of%25202%252C%252075gms%2520each%2520%257C%2520pH%25205.5%252C%2520with%2520Oatmeal%2520Powder%252C%2520Shea%2520Butter%252C%2520Aloe%2520Vera%2520%2526%2520Calendula%2520Oil%2520%257C%2520Allergen%2520Free%2520%257C%2520Dermatologically%2520Tested