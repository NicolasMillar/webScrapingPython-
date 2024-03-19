import psycopg2 
import os 
from dotenv import load_dotenv
from common import getBox, getDataApi, getCardId, insertData

base_url = 'https://www.guildreams.com'

def getCardsInfo(box, connection, cardsDB):
    if box:
        cards = box.find_all('div', class_='bs-product')

        for card in cards:
            card_name = card.find('h2', class_='text-truncate mt-2 h6').text.strip()
            card_price = card.find('div', class_='bs-product-final-price').text.strip()
            card_url = base_url + card.find('div', class_='bs-product-info').find('a')['href']
            card_id = getCardId(card_name, cardsDB)

            insertData(connection, 1, card_id, card_price, card_url)

def getCardsList(limit, Baseurl, booster, connection, cards):
    for page in range(1, limit+1):
        url = f'{Baseurl}{page}'
        box = getBox(url)
        getCardsInfo(box, connection, cards)
        print(f"pagina: {page} del booster: {booster} completada")

load_dotenv()
try:
    connection = psycopg2.connect(
        dbname=os.getenv('db_name'),
        user=os.getenv('db_user'),
        password=os.getenv('db_password'),
        host=os.getenv('db_host'),
        port=os.getenv('db_port', 5432)
    )

    print("Conexion realizada con exito")
    cards = getDataApi();
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt1-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt1', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt2-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt2', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt3-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt3', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt4-great-legend?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt4', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt5-battle-of-omni?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt5', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt6-double-diamond?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt6', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt7-next-adventure?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt7', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt8-new-awakening?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt8', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt9-x-record?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt9', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt10-xros-encounter?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt10', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt11-dimensional-phase?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt11', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt12-across-time?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt12', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt13-versus-royal-knights?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt13', connection, cards)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt14-blast-ace?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14', connection, cards)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex1-classic-collection?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex1', connection, cards)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex2-digital-hazard?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex2', connection, cards)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex3-draconic-roar?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex3', connection, cards)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex4-alternative-being?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex4', connection, cards)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex5-animal-colosseum?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex5',connection, cards) 

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")