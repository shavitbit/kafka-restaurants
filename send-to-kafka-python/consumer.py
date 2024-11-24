from kafka import KafkaProducer, KafkaConsumer
consumer = KafkaConsumer('weather_data_demo', bootstrap_servers='localhost:32001')

print("Gonna start listening")
while True:
    for message in consumer:
        print("Here is a message..")
        print (message)