# Excute the following commands to startup the project

- From the root of the project switch to the deployment directory. `cd deployment`
- Run `kubectl apply -f zookeeper.yaml` to install zookeeper and zookeeper-service.
- Run `kubectl get services zookeeper-service | grep zookeeper-service | awk '{ print $3 }'` to get the zookeeper ip address.
- Edit kafka.yaml and replace KAFKA_ZOOKEEPER_IP (line 39) with the IP returned from the previous step. Save the file.
- Run `kubectl apply -f kafka.yaml`
- Run `kubectl get pods | grep kafka-broker | awk '{print $1}'` to get the name of the kafka-broker pod. You will use this in the next step.
- Run `kubectl exec --stdin --tty <kafka pod name> -- /bin/bash`
  - In the prompt that opens execute:
     - `/opt/kafka_2.13-2.8.1/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic locations` To create the 'locations' topic within kafka.
     - Optional `/opt/kafka_2.13-2.8.1/bin/kafka-topics.sh --list --bootstrap-server localhost:9092` can be used to check for the newly created topic.
  - Execute `exit` on the command line to exit the bash terminal in the pod and return to your local command line.
- Run `kubectl apply -f db-configmap.yaml`
- Run `kubectl apply -f db-secret.yaml`
- Run `kubectl apply -f postgres.yaml`
- Run `kubectl apply -f udaconnect-app.yaml`
- Run `kubectl apply -f grpc-connections.yaml`
- Run `kubectl apply -f udaconnect-connections.yaml`
- Run `kubectl apply -f udaconnect-persons.yaml`
- Run `kubectl apply -f udaconnect-locations.yaml`
- Run `kubectl apply -f udaconnect-locations-consumer.yaml`

# Design

Get starter project running from my account as is.

Break up the current application into 3 microservices.

- Location
- Person
- Connections

Persons api: http://localhost:30001/api/persons

Added api build to github actions.

