# Email system
import time
from kafka import KafkaConsumer
import json
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
bootstrap_svr = os.getenv('BOOTSTRAP_SVR')

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'order_confirm',
    bootstrap_servers= bootstrap_svr,
    group_id='confirmation-service',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def send_mail_confirmation():
    logger.info("Starting to listen to Kafka messages...")

    for message in consumer:
        logger.info("Received a message from Kafka.")
        try:
            if isinstance(message.value, list):  
                for item in message.value:
                    if isinstance(item, dict) and 'email' in item: 
                        to = item['email']
                        logger.info(f"Sending mail confirmation to: {to}")
                        consumer.commit()
                    else:
                        logger.warning("Item in list is not a dictionary or missing 'email' key.")
                        consumer.commit()
            else:
                logger.error("Message value is not a list.")
                consumer.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
    
# This program simulates this function.

#    def send_email(to, subject, message):
#    try:
#        email_address = os.environ.get("EMAIL_ADDRESS")
#        email_password = os.environ.get("EMAIL_PASSWORD")
#
#        if email_address is None or email_password is None:
#            # no email address or password
#            # something is not configured properly
#            print("Did you set email address and password correctly?")
#            return False
#
#        # create email
#        msg = EmailMessage()
#        msg['Subject'] = subject
#        msg['From'] = email_address
#        msg['To'] = to
#        msg.set_content(message)
#
#        # send email
#        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#            smtp.login(email_address, email_password)
#            smtp.send_message(msg)
#        return True
#    except Exception as e:
#        print("Problem during send email")
#        print(str(e))
#    return False


# Main
while True:
    time.sleep(1) 
    send_mail_confirmation()