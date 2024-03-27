from bs4 import BeautifulSoup
import requests
import Levenshtein
import os

def getBox(url, container, Searchclass):
    website = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    result = requests.get(website, headers=headers)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')
    box = soup.find(container, class_=Searchclass)

    return box

def getDataApi():
    api_url = os.getenv('api_url')

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data;
        else:
            return {'error': f'Status Code: {response.status_code}, {response.text}'}

    except requests.RequestException as e:
        return {'error': str(e)}
    
def getCardId(name, cards):
    filter_cards = [card for card in cards if name.lower() in card['nombre'].lower()]
    id = calculate_similarity(name, filter_cards)
    return id

def calculate_similarity(card_name, cards):
    max_similarity = 0
    id = 0

    for card in cards:
        name = card.get('nombre')
        similarity = Levenshtein.ratio(card_name.lower(), name.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            id = card.get('id')

    if(id == 0):
        id = cards[0].get('id')

    return id

def insertData(connection, id_tienda, id_card, price, card_url):
    try:
        with connection.cursor() as cursor:
            sql_insert_or_update_carta = """
                INSERT INTO Carta (id_carta, id_tienda, precio, card_url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_carta, id_tienda)
                DO UPDATE SET precio = EXCLUDED.precio, card_url = EXCLUDED.card_url
                RETURNING id_carta;
            """
            cursor.execute(sql_insert_or_update_carta, (id_card, id_tienda, price, card_url))

        connection.commit()
    except Exception as e:
        print(f"Error durante la inserción o actualización: {id_card, id_tienda, e}")