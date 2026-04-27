import psycopg2
from config import DB_CONFIG

# просто подключаемся к базе данных
def get_connection():
    return psycopg2.connect(**DB_CONFIG)