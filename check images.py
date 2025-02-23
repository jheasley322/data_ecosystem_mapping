import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20230606165706/https://www.instana.com/supported-technologies/"
response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")
    
    # Print all found image URLs
    for img in img_tags:
        print(img.get("src"))

else:
    print(f"Failed to fetch page, status code: {response.status_code}")