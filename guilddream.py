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

def getCardsInfo(box, booster, connection):
    if box:
        cards = box.find_all('div', class_='bs-product')

        for card in cards:
            card_name = card.find('h2', class_='text-truncate mt-2 h6').text.strip()
            card_img = card.find('img').get('data-src')


def getCardsList(limit, Baseurl, booster, connection):
    for page in range(1, limit+1):
        url = f'{Baseurl}{page}'
        box = getBox(url)
        getCardsInfo(box, booster, connection)

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

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")