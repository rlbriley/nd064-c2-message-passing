# Design

Get starter project running from my account as is.

Break up the current application into 3 microservices.

- Location
- Person
- Connections

Persons api: http://localhost:30001/api/persons

Added api build to github actions.

- run `kubectlfka apply -f zookeeper.yaml`
- run `kubectl get services -n kafka`
- run `kubectl get services -n kafka | grep zookeeper-service | awk '{ print $3 }'` to get the zookeeper ip address.
- Edit kafka.yaml and replace the ipaddress in KAFKA_ZOOKEEPER_CONNECT (line 37). Save the file.
- run `kubectl apply -f kafka.yaml`
- Add "127.0.0.1 kafka-broker" to  C:\Windows\System32\drivers\etc\hosts
- run `kubectl port-forward <kafka pod name> 9092 -n kafka`
- Install kafka locally.
- `kafka-topics.bat --create --topic locations --bootstrap-server localhost:9092`


