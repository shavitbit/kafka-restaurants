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

logger.info("Kafka Consumer initialized for topic 'order'.")

def confirm_transaction():
    logger.info("Starting to listen to Kafka messages...")

    for message in consumer:
        logger.info("Received a message from Kafka.")
        try:
            data = message.value
            logger.debug(f"Message data: {data}")
            
            # Validate credit card
            if 'credit_card' in data and len(data['credit_card']) == 16:
                logger.info("Valid credit card detected.")
                logger.info("Order processed successfully:" + json.dumps(data))
            else:
                logger.warning("Invalid credit card number: " + json.dumps(data))
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)

logger.info("Starting the application loop...")
while True:
    time.sleep(1)
    logger.debug("Waiting for the next message...")
    confirm_transaction()