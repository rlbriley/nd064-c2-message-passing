# Design

Get starter project running from my account as is.

Break up the current application into 3 microservices.

- Location
- Person
- Connections

Persons api: http://localhost:30001/api/persons

Added api build to github actions.

- Run `kubectl apply -f zookeeper.yaml` to install zookeeper and zookeeper-service.
- Run `kubectl get services zookeeper-service | grep zookeeper-service | awk '{ print $3 }'` to get the zookeeper ip address.
- Edit kafka.yaml and replace the ipaddress in KAFKA_ZOOKEEPER_CONNECT (line 37) with the IP returned from the previous step. Save the file.
- run `kubectl apply -f kafka.yaml`
- Add "127.0.0.1 kafka-broker" to  C:\Windows\System32\drivers\etc\hosts
- Run `kubectl port-forward <kafka pod name> 9092` in a separate window. Because it will keep running as long as it is forwarding the port.
- Install kafka locally.
- Run `kafka-topics.bat --create --topic locations --bootstrap-server localhost:9092` to create the 'locations' topic in kafka.
   <br/>Optional `kafka-topics.bat --list --bootstrap-server localhost:9092` can be used to check for the newly created topic.


