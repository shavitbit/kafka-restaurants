# Kafka restaurants system (still in development)

Kafka Restaurants is a buying and delivery system designed to demonstrate how to build and work with Kafka and other microservices on Kubernetes.

The user accesses the website, and the load balancer directs them to one of the frontend replicas. On the site, the user can search for a restaurant and place an order. The search and order actions are handled by a backend API microservice, which processes the order by validating it and initiating a transaction with the bank. If the order is successfully verified, the user receives a confirmation email.

The search and order microservice acts as the producer for the Order topic, while the transaction microservice is the consumer. After completing the transaction, the transaction microservice becomes the producer for the Order_Confirm topic, and the email microservice serves as its consumer.

I didn't have enough memory in Minikube to add a real database,
so I used a ConfigMap.
The credit card system and SMTP server, which are outside the diagram, are mocked.

![Kafka restaurants system diagram](/media/system%20diagram.png) 

## FrontEnd

    <img
        src="/media/frontend.png" 
        width=70%
        title="Search for restaurant"
        alt="Search for restaurant"
    />



