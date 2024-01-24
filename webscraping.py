from bs4 import BeautifulSoup
import requests
import psycopg2 
import os 
from dotenv import load_dotenv

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

def getCardsList(limit, Baseurl, booster):
    all_cards_list = []

    for page in range(1, limit+1):
        url = f'{Baseurl}{page}'
        box = getBox(url)
        cards_list = getCardsInfo(box, booster)
        all_cards_list.extend(cards_list)

    return all_cards_list


"""  cardsBt1 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt1-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt1')
cardsBt2 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt2-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt2')
cardsBt3 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt3-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt3')
cardsBt4 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt4-great-legend?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt4')
cardsBt5 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt5-battle-of-omni?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt5')
cardsBt6 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt6-double-diamond?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt6')
cardsBt7 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt7-next-adventure?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt7')
cardsBt8 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt8-new-awakening?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt8')
cardsBt9 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt9-x-record?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt9')
cardsBt10 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt10-xros-encounter?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt10')
cardsBt11 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt11-dimensional-phase?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt11')
cardsBt12 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt12-across-time?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt12')
cardsBt13 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt13-versus-royal-knights?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt13')
cardsBt14 = getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt14-blast-ace?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14')
cardsEx1 = getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex1-classic-collection?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14')
cardsEx2 = getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex2-digital-hazard?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14')
cardsEx3 = getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex3-draconic-roar?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14')
cardsEx4 = getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex4-alternative-being?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14')
cardsEx5 = getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex5-animal-colosseum?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14')  """

load_dotenv()
try:
    connection = psycopg2.connect(
        dbname=os.getenv('db_name'),
        user=os.getenv('db_user'),
        password=os.getenv('db_password'),
        host=os.getenv('db_host'),
        port=os.getenv('db_port', 5432)
    )
    
    print("Conexión exitosa!")

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")