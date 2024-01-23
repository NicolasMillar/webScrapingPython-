from bs4 import BeautifulSoup
import requests

website = 'https://www.guildreams.com/collection/digimon-bt1-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
result = requests.get(website, headers=headers)
content = result.text

soup = BeautifulSoup(content, 'lxml')
box = soup.find('article', class_='col-lg-9')
products_list = []

if box:
    cards = box.find_all('div', class_='bs-product')

    for card in cards:
        card_name = card.find('h2', class_='text-truncate mt-2 h6').text.strip()
        print(card_name)