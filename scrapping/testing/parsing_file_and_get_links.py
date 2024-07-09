file_name ="/home/nandhakumar/nandha_naturals/scrapping/sample.txt"
from bs4 import BeautifulSoup

# Step 1: Read the contents of the text file
file_path = file_name  # Replace with your file path
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Step 2: Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
links = soup.select("h3.flex.flex-col.xl\\:gap-1.lg\\:gap-0.5 a.h-full")

# Extract href attributes from <a> tags
links = [link.get('href') for link in links]

# Print the extracted links
print(links)
