# Kafka restaurants system (still in development)

Kafka Restaurants is a buying and delivery system designed to demonstrate how to build and work with Kafka and other microservices on Kubernetes.

The user accesses the website, and the load balancer directs them to one of the frontend replicas. On the site, the user can search for a restaurant and place an order. The search and order actions are handled by a backend API microservice, which processes the order by validating it and initiating a transaction with the bank. If the order is successfully verified, the user receives a confirmation email.

The search and order microservice acts as the producer for the Order topic, while the transaction microservice is the consumer. After completing the transaction, the transaction microservice becomes the producer for the Order_Confirm topic, and the email microservice serves as its consumer.

I didn't have enough memory in Minikube to add a real database,
so I used a ConfigMap.
The credit card system and SMTP server, which are outside the diagram, are mocked.

![Kafka restaurants system diagram](/media/system%20diagram.png) 

## FrontEnd

![Search for restaurant|200](/media/frontend.png)




## Kafka code explanation

Producer <br/>
1. Load the Kafka package with KafkaProducer to connect to and work with Kafka as a producer.
2. Load the dotenv and os packages to use environment variables for the bootstrap server.
3. Initialize the producer and configure it with the bootstrap server.
4. Produce or send messages to the topic "order_confirm" in JSON format, encoding them in UTF-8.
```py
from kafka import KafkaProducer
import os
from dotenv import load_dotenv

load_dotenv()

bootstrap_svr = os.getenv('BOOTSTRAP_SVR') 

producer = KafkaProducer(
    bootstrap_servers=bootstrap_svr
)
data = [
     {
        "somedata": 1,
        "moredata": "data",
        "email": "oren@example.com"
    }# list of data
]  

producer.send("order_confirm", json.dumps(data).encode("utf-8"))
```

Consumer <br/>
1. Load the Kafka package with KafkaConsume to connect to and work with Kafka as a producer.
2. Load the dotenv and os packages to use environment variables for the bootstrap server.
3. Initialize the consumer and configure it with the bootstrap server.
    * <b>order</b> = Topic Name. 
    * <b>group_id</b> = Kafka tracks offsets (the position of messages in a topic) for each consumer group independently. Consumers within the same group divide the messages in a topic among themselves. Each message is processed by only one consumer in the group
    * <b>auto_offset_reset</b> = Determines what happens when a consumer starts and there is no committed offset for the topic/partition in the specified group. Value earliest: Start consuming from the beginning of the topic (the oldest available message).
    * <b>enable_auto_commit</b> = Determines whether Kafka automatically commits offsets for messages as they are consumed. Value False: You must manually commit offsets using consumer.commit()
4. After processing and handling the data, commit the consumer.  Kafka is used to commit the offset for the messages that a consumer has successfully processed.
```python
from kafka import KafkaConsumer
import os
from dotenv import load_dotenv

load_dotenv()
bootstrap_svr = os.getenv('BOOTSTRAP_SVR') 

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'order',
    bootstrap_servers=bootstrap_svr,
    group_id='transaction-service',  # Consumer group ID
    auto_offset_reset='earliest',   # Start from the earliest offset
    enable_auto_commit=False,        # Manually commit offsets
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Code and data processing to handle the data... 
# ...

consumer.commit()

```