   #transaction system
#from flask import Flask, request, jsonify
import time
from kafka import KafkaProducer, KafkaConsumer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'order',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092"
)

logger.info("Kafka Consumer initialized for topic 'order'.")
logger.info("Kafka producer initialized for topic 'order_confirm'.")

def confirm_transaction():
    logger.info("Starting to listen to Kafka messages...")

    for message in consumer:
        logger.info("Received a message from Kafka.")
        varified_data= []
        try:
            data = message.value
            logger.debug(f"Message data: {data}")
            
            # Validate credit card (in the real world it will validate with the banking system)
            if 'credit_card' in data and len(data['credit_card']) == 16:
                logger.info("Valid credit card detected.")
                logger.info("Order processed successfully:" + json.dumps(data))
                varified_data.append(data)
            else:
                logger.warning("Invalid credit card number: " + json.dumps(data))
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
        return varified_data





def produce_verified_order(data):
    logger.info("Starting to producing to Kafka messages...")
    producer.send("order_confirm", json.dumps(data).encode("utf-8"))
    print(f"Done Sending..")
    time.sleep(1)


logger.info("Starting application loop...")
while True:
    time.sleep(1)
    logger.debug("Waiting for the next message...")
    data = confirm_transaction()
    if data:
        logger.debug("Waiting to produce the message")
        logger.info(data)
        produce_verified_order(data)