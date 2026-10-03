from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Only 20 users, so each user gets many transactions
user_profiles = {uid: random.randint(50, 300) for uid in range(1, 21)}

while True:
    user_id = random.randint(1, 20)
    base_amount = user_profiles[user_id]
    
    if random.random() < 0.90:
        amount = max(1, int(random.gauss(base_amount, base_amount * 0.1)))
    else:
        if random.random() < 0.5:
            amount = base_amount * random.randint(10, 20)
        else:
            amount = max(1, base_amount // random.randint(10, 20))
    
    data = {"user_id": user_id, "amount": amount}
    producer.send('transactions', data)
    print(f"Sent: {data}")
    time.sleep(0.5)   # Faster: 2 transactions per second