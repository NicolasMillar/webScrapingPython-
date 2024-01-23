from bs4 import BeautifulSoup
import requests
import time

def getBox(url):
    website = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    result = requests.get(website, headers=headers)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article', class_='col-lg-9')

    return box

def getCardsInfo(box, booster):
    cards_list = []
    if box:
        cards = box.find_all('div', class_='bs-product')

        for card in cards:
            card_name = card.find('h2', class_='text-truncate mt-2 h6').text.strip()
            card_img = card.find('img').get('data-src')

            card_info = {
                'name' : card_name,
                'img' : card_img,
                'booster' : booster
            }
            
            cards_list.append(card_info)

    return cards_list

def getCardsList(limit):
    all_cards_list = []
    for page in range(1, limit+1):
        url = f'https://www.guildreams.com/collection/digimon-bt1-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&&page={page}'
        box = getBox(url)
        cards_list = getCardsInfo(box, 'bt1')
        all_cards_list.extend(cards_list)

    return all_cards_list


cardsList = getCardsList(7)
print(f"Numero de cartas guardads: {len(cardsList)}")