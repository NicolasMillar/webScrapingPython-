import psycopg2 
import os
import re
from dotenv import load_dotenv
from common import getBox,getDataApi, getCardId, insertData

load_dotenv()
baseUrl = 'https://www.deckscards.cl/'

def getCardsList(limit, url, booster, cards, connection):
    for page in range(1, limit+1):
        pageUrl = f'{url}{page}'
        box = getBox(pageUrl, 'div', 'box-product row')
        getCardsInfo(box, cards, connection)
        print(f"pagina: {page} del booster: {booster} completada")

def getCardsInfo(box, cardsDb, connection):
    if box:
        cards = box.find_all('div', class_='col-md-4 col-xs-6')

        for card in cards:
            aux = card.find('h3', class_= 'product-name').a
            card_name = aux.text.strip()
            unwanted_words = ["Digimon", "Option", "Digi-Egg", "Tamer", " C", " U", " R", " SR", " SEC", " PR"] 
            for word in unwanted_words:
                card_name = re.sub(r'\b' + re.escape(word) + r'\b', '', card_name)
            card_name = re.sub(r'\s+', ' ', card_name).strip()
            if "(Holo)" in card_name:
                card_name = re.sub(r'(\s-\sP-\d{3})\s\(Holo\)', r' (Foil)\1', card_name)

            card_url = baseUrl + aux['href']
            card_price = card.find('span', class_= 'final_price').text.strip().replace('CLP', '').rstrip()
            card_id = getCardId(card_name, cardsDb)
            
            if(card_id != 0):
                insertData(connection, 2, card_id, card_price, card_url)
            else:
                print("Error con" + card_name)

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
    getCardsList(3, 'https://www.deckscards.cl/digimon/booster-ver10?sorting=name-asc&page=', 'bt1', cards, connection)
    getCardsList(4, 'https://www.deckscards.cl/booster-ver-15?sorting=name-asc&page=', 'bt2', cards, connection)
    getCardsList(5, 'https://www.deckscards.cl/digimon/bt4?sorting=name-asc&page=', 'bt4', cards, connection)
    getCardsList(4, 'https://www.deckscards.cl/digimon/bt5?sorting=name-asc&page=', 'bt5', cards, connection)
    getCardsList(3, 'https://www.deckscards.cl/digimon/bt6?sorting=name-asc&page=', 'bt6', cards, connection)
    getCardsList(3, 'https://www.deckscards.cl/digimon/ediciones/bt7?sorting=name-asc&page=', 'bt7', cards, connection)
    getCardsList(3, 'https://www.deckscards.cl/digimon/ediciones/bt8?sorting=name-asc&page=', 'bt8', cards, connection)
    getCardsList(3, 'https://www.deckscards.cl/bt9?sorting=name-asc&page=', 'bt9', cards, connection)
    getCardsList(3, 'https://www.deckscards.cl/bt10?sorting=name-asc&page=', 'bt10', cards, connection)
    getCardsList(2, 'https://www.deckscards.cl/digimon/ediciones/bt-11-booster-dimensional-phase?sorting=name-asc&page=', 'bt11', cards, connection)
    getCardsList(4, 'https://www.deckscards.cl/digimon/ediciones/bt-12-across-time?sorting=name-asc&page=', 'bt12', cards, connection)
    getCardsList(3, 'https://www.deckscards.cl/digimon/ediciones/bt13-versus-royal-knights?sorting=name-asc&page=', 'bt13', cards, connection)
    getCardsList(3, 'https://www.deckscards.cl/digimon/ediciones/2023/bt14-blast-ace?sorting=name-asc&page=', 'bt14', cards, connection)
    getCardsList(2, 'https://www.deckscards.cl/digimon/ediciones/classic-collection-ex-01?sorting=name-asc&page=', 'ex1', cards, connection)
    getCardsList(2, 'https://www.deckscards.cl/digimon/ediciones/ex-02?sorting=name-asc&page=', 'ex2', cards, connection)
    getCardsList(2, 'https://www.deckscards.cl/digimon/ediciones/ex-03-draconic-roar?sorting=name-asc&page=', 'ex3', cards, connection)
    getCardsList(2, 'https://www.deckscards.cl/digimon/ediciones/ex04-alternative-being?sorting=name-asc&page=', 'ex4', cards, connection)
    getCardsList(4, 'https://www.deckscards.cl/digimon/ediciones/2024/ex-05-animal-colosseum?sorting=name-asc&page=', 'ex5', cards, connection)

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")