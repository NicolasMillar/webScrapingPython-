import psycopg2 
import os
import re
from dotenv import load_dotenv
from common import getBox,getDataApi, getCardId, insertData

load_dotenv()
baseUrl = 'https://www.deckscards.cl/'

def getCardsList(limit, url, booster, cards):
    for page in range(1, limit+1):
        pageUrl = f'{url}{page}'
        box = getBox(pageUrl, 'div', 'box-product row')
        getCardsInfo(box, cards)
        print(f"pagina: {page} del booster: {booster} completada")

def getCardsInfo(box, cardsDb):
    if box:
        cards = box.find_all('div', class_='col-md-4 col-xs-6')

        for card in cards:
            aux = card.find('h3', class_= 'product-name').a
            card_name = aux.text.strip()
            unwanted_words = ["Digimon", "Option", "Digi-Egg", "Tamer", "C", "U", "R", "SR", "SEC", "PR"] 
            for word in unwanted_words:
                card_name = card_name.replace(word, '').rstrip()
            card_name = re.sub(r'\s+', ' ', card_name).strip()
            card_url = baseUrl + aux['href']
            card_price = card.find('span', class_= 'final_price').text.strip().replace('CLP', '').rstrip()
            
            print(card_name)

try:
    connection = psycopg2.connect(
        dbname=os.getenv('db_name'),
        user=os.getenv('db_user'),
        password=os.getenv('db_password'),
        host=os.getenv('db_host'),
        port=os.getenv('db_port', 5432)
    )

    print("Conexion realizada con exito")
    cards = getDataApi()
    getCardsList(3, 'https://www.deckscards.cl/digimon/booster-ver10?sorting=name-asc&page=', 'bt1', cards)

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")