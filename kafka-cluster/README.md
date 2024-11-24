To start the installation of Kafka on Minikube, I chose to use the Strimzi CRD to create a simple development environment.
```sh
kubectl create namespace kafka
kubectl config set-context --current --namespace=kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
```

Apply my custom YAML file to configure the cluster:
```sh
kubectl apply -f kafka-cluster.yaml -n kafka
```

Test the cluster by entering the Kafka pod and running the following commands:
```sh
cd bin
./kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic
```
Enter some messages, then run the consumer command:
```sh
./kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
```
