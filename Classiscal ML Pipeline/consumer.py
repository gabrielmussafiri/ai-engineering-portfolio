from kafka import KafkaConsumer
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# 1. Connect to PostgreSQL
conn = psycopg2.connect(
    db_name = DB_NAME,
    user = DB_USER,
    password = DB_PASSWORD,
    host = DB_HOST,
    port = DB_PORT
)

cursor = conn.cursor()

# 2. Connect To Kafka
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

# 3. For Each message, insert to db
for message in consumer:
    data = message.value
    cursor.execute(
        "INSERT INTO transactions (user_id, amount)VALUES(%s,%s)",
        (data['user_id'],data['amount'])
    )
    conn.commit()
    print(f"Insert: {data}")