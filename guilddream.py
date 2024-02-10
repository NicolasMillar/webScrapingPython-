from bs4 import BeautifulSoup
import requests
import psycopg2 
import Levenshtein
import os 
from dotenv import load_dotenv

base_url = 'https://www.guildreams.com'

def getBox(url):
    website = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    result = requests.get(website, headers=headers)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article', class_='col-lg-9')

    return box

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
        print("pagina: "+page+" del booster: "+booster +" completada")

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
    

def calculate_similarity(card_name, cards):
    max_similarity = 0.8
    id = 0

    for card in cards:
        name = card.get('nombre')
        similarity = Levenshtein.ratio(card_name.lower(), name.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            id = card.get('id')
    return id

def insertData(connection, id_tienda, id_card, price, card_url):
    try:
        with connection.cursor() as cursor:
            sql_insert_or_update_carta = """
                INSERT INTO Carta (id_carta, id_tienda, precio, card_url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_carta, id_tienda)
                DO UPDATE SET precio = EXCLUDED.precio, card_url = EXCLUDED.card_url
                RETURNING id;
            """
            cursor.execute(sql_insert_or_update_carta, (id_card, id_tienda, price, card_url))

        connection.commit()
    except Exception as e:
        print(f"Error durante la inserción o actualización: {id_card, id_tienda, e}")

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

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")