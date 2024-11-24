import json
import time

from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = "weather_data_demo"
ORDER_LIMIT = 15

producer = KafkaProducer(bootstrap_servers="localhost:9092")

print("Going to be generating order after 10 seconds")
print("Will generate one unique order every 5 seconds")
time.sleep(10)

for i in range(ORDER_LIMIT):
    data = {
        "order_id": i,
        "user_id": f"tom_{i}",
        "total_cost": i,
        "items": "burger,sandwich",
    }

    producer.send(ORDER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
    print(f"Done Sending..{i}")
    time.sleep(5)