from kafka import KafkaProducer
import json , time , random

producer = KafkaProducer(
    bootstrap_servers ='localhost:9092',
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data ={"user_id":random.randint(1,100),"amount":random.randint(1,500)}
    producer.send('transactions',data)
    print(f'sent: {data}')
    time.sleep(2)
    