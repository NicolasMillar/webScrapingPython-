import requests
import psycopg2 
import os 
from dotenv import load_dotenv
from common import getBox, calculate_similarity, insertData

base_url = 'https://www.guildreams.com'

def getCardsInfo(box, booster, connection):
    if box:
        cards = box.find_all('div', class_='bs-product')

        for card in cards:
            card_name = card.find('h2', class_='text-truncate mt-2 h6').text.strip()
            card_price = card.find('div', class_='bs-product-final-price').text.strip()
            card_url = base_url + card.find('div', class_='bs-product-info').find('a')['href']
            card_id = getDataApi(card_name, booster)
            
            insertData(connection, 1, card_id, card_price, card_url)

def getCardsList(limit, Baseurl, booster, connection):
    for page in range(1, limit+1):
        url = f'{Baseurl}{page}'
        box = getBox(url)
        getCardsInfo(box, booster, connection)
        print(f"pagina: {page} del booster: {booster} completada")

def getDataApi(name, booster):
    api_url = os.getenv('api_url')
    params = {'cardName': name, 'booster': booster}

    try:
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()

            if len(data) == 1:
                return data[0].get('id')
            else:
                newId = calculate_similarity(name, data)
                return newId
        else:
            return {'error': f'Status Code: {response.status_code}, {response.text}'}

    except requests.RequestException as e:
        return {'error': str(e)}

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
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt1-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt1', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt2-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt2', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt3-release-special?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt3', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt4-great-legend?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt4', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt5-battle-of-omni?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt5', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt6-double-diamond?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt6', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt7-next-adventure?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt7', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt8-new-awakening?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt8', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt9-x-record?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt9', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt10-xros-encounter?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt10', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt11-dimensional-phase?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt11', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt12-across-time?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt12', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt13-versus-royal-knights?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt13', connection)
    getCardsList(7, 'https://www.guildreams.com/collection/digimon-bt14-blast-ace?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'bt14', connection)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex1-classic-collection?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex1', connection)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex2-digital-hazard?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex2', connection)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex3-draconic-roar?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex3', connection)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex4-alternative-being?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex4', connection)
    getCardsList(4, 'https://www.guildreams.com/collection/digimon-ex5-animal-colosseum?limit=24&with_stock=0&smart_stock=0&order=name&way=ASC&page=', 'ex5',connection) 

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")