import psycopg2 
import os 
from dotenv import load_dotenv
from common import getBox,getDataApi, getCardId, insertData
from bs4 import BeautifulSoup
import requests

load_dotenv()


def getCardsList(limit, url, booster):
    for page in range(1, limit+1):
        pageUrl = f'{url}{page}'
        box = getBox(pageUrl, 'div', 'box-product row')
        print(box)

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
    getCardsList(3, 'https://www.deckscards.cl/digimon/booster-ver10?sorting=name-asc&page=', 'bt1')

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")