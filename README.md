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

## Key Security Considerations When Deploying the Frontend Microservice on Kubernetes
### Challenges
1. <b> Backend API Accessibility </b> <br/>
   As illustrated in the Kubernetes architecture, the backend APIs (search and orders) are not accessible outside the cluster. However, frontend JavaScript executes requests from the user's browser, which cannot directly connect to the backend.
2. <b>Incorrect Backend URL</b> </br>
      The hardcoded const url in the frontend JavaScript code is incorrect when deployed on Kubernetes. This issue causes the frontend to fail when trying to connect to the backend APIs.

```javascript
try {
        const url = 'http://127.0.0.1:5000'
        const response = await fetch(`${url}/search?${queryParams.toString()}`);
        const data = await response.json();

```
### Solution: Dynamic URL Configuration

To resolve the URL issue, I created a Bash script as the container's entrypoint in the Dockerfile and configured the environment variable via the Helm chart.

<b>Entrypoint Script in Dockerfile:</b>
```sh
# Check if URL is set, else use a default value
API_URL=${API_URL:-http://127.0.0.1:5000}

# Replace the URL in the JavaScript file
sed -i "s|const url = 'http://127.0.0.1:5000'|const url = '${API_URL}'|" /usr/share/nginx/html/script.js
sed -i "s|const url = 'http://127.0.0.1:5000'|const url = '${API_URL}'|" /usr/share/nginx/html/orders.html

# Start Nginx
nginx -g "daemon off;"
```
<b>Helm Chart Configuration (values.yaml):</b>
```yaml
backend:
  env:
    BOOTSTRAP_SVR: my-cluster-kafka-plain-bootstrap.kafka.svc.cluster.local:9092
  apiUrl: "http://searchorder-web-svc:5000"
```

### Solution: Proxy Requests Through NGINX
To ensure the user cannot directly access the backend API, I configured a proxy in the NGINX server, Updated the default.conf file to redirect frontend requests to the backend API and modified the apiUrl in values.yaml to use /api as the base URL.

<b>NGINX Configuration (default.conf):</b>
```nginx
        
        # Proxy API requests to the internal service
        
        location /api/ {
            rewrite ^/api/(.*)$ /$1 break;  # Remove the '/api' prefix
            proxy_pass http://searchorder-web-svc:5000/;  # Internal service
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
```
<b>Update values.yaml:</b>
```yaml
backend:
  apiUrl: "/api"
```



## Kafka code concepts

<b>Producer</b> <br/>
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

<b>Consumer</b> <br/>
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
## Docker
```sh
docker build -t frontend:0.0.1 -f .\docker\dockerfile-frontend .
docker build -t searchorder:0.0.1 -f .\docker\dockerfile-flask .  
docker build -t transactions:0.0.1 -f .\docker\dockerfile-transactions .
docker build -t pymail:0.0.1 -f .\docker\dockerfile-pymail .
# tag all images with my docker user philipsinfo/<image-name:version> 
# and push them to my public repository so i can pull them from the helm chart.
```

## Kubernetes

### Strimzi CRD
To set up Kafka on Minikube, I utilized Strimzi CRDs to simplify the installation process and create a minimal environment. Detailed installation steps are documented in the readme.md file located in the kafka-cluster folder.
* When testing applications hosted on local machine (outside of Kubernetes), I to exposed the Kafka cluster using a LoadBalancer. To achieve this, I modified the values.yaml configuration for Strimzi, setting the listener type to LoadBalancer
* For both Kafka and the consuming/producing applications are running inside the Kubernetes cluster, additional listener configuration is required. Use the advertisedHost field in the Kafka listener configuration to ensure proper communication. The advertisedHost should point to the Kafka service's bootstrap address.

```yaml
spec:
  kafka:
    version: 3.7.0
    replicas: 1 
    listeners:
      - name: plain
        port: 9092
        configuration:
         brokers: 
         - broker: 0
           advertisedHost: my-cluster-kafka-plain-bootstrap.kafka.svc.cluster.local
           advertisedPort: 9092
        type: ClusterIP # or loadbalancer
```
### Helm Chart
The helm chart configutation located in the helm folder and it contains:
* ConfigMap-data as the restaurants database
* Nginx-config that replace the default.conf file for the frontend microsecvice 
* Horizontal pod autoscaler for the backend api and for the frontend deployment
* Servic for the frontend as a LoadBalancer and service for the backend api as a ClusterIP
* Deployments for frontend, backend api, transactions app, and email app.
```sh
cd helm
helm install kafka-restaurants .
```
### ArgoCD