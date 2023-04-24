# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### Technologies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster

## Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
4. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
5. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`.
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Steps
1. From the root of the project switch to the deployment directory. `cd deployment`
1. Run `kubectl apply -f zookeeper.yaml` to install zookeeper and zookeeper-service.
1. Run `kubectl get services zookeeper-service | grep zookeeper-service | awk '{ print $3 }'` to get the zookeeper ip address.
1. Edit kafka.yaml and replace KAFKA_ZOOKEEPER_IP (line 39) with the IP returned from the previous step. Save the file.
1. Run `kubectl apply -f kafka.yaml`
1. Run `kubectl get pods | grep kafka-broker | awk '{print $1}'` to get the name of the kafka-broker pod. You will use this in the next step.
1. Run `kubectl exec --stdin --tty <kafka pod name> -- /bin/bash`
   - In the prompt that opens execute:
      - `/opt/kafka_2.13-2.8.1/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic locations` To create the 'locations' topic within kafka.
      - Optional `/opt/kafka_2.13-2.8.1/bin/kafka-topics.sh --list --bootstrap-server localhost:9092` can be used to check for the newly created topic.
   - Execute `exit` on the command line to exit the bash terminal in the pod and return to your local command line.
1. Run `kubectl apply -f db-configmap.yaml`
1. Run `kubectl apply -f db-secret.yaml`
1. Run `kubectl apply -f postgres.yaml`
1. Run `kubectl apply -f udaconnect-app.yaml`
1. Run `kubectl apply -f grpc-connections.yaml`
1. Run `kubectl apply -f udaconnect-connections.yaml`
1. Run `kubectl apply -f udaconnect-persons.yaml`
1. Run `kubectl apply -f udaconnect-locations.yaml`
1. Run `kubectl apply -f udaconnect-locations-consumer.yaml`

Manually applying each of the individual `yaml` files is cumbersome but going through each step provides some context on the content of the project. In practice, we would have reduced the number of steps by running the command against a directory to apply of the contents: `kubectl apply -f deployment/`.

Note: The first time you run this project, you will need to seed the database with dummy data. Use the command `sh scripts/run_db_command.sh` against the `postgres` pod. Subsequent runs of `kubectl apply` for making changes to deployments or services shouldn't require you to seed the database again!

### Verifying it Works
Once the project is up and running, you should be able to see 9 deployments and 9 services in Kubernetes:
`kubectl get pods` and `kubectl get services` - should both return:
- udaconnect-app
- udaconnect-connections
- grpc-connections
- udaconnect-locations
- udaconnect-locations-consumer
- udaconnect-persons
- kafka-broker
- postgres


These pages should also load on your web browser:
* `http://localhost:30002/` - persons OpenAPI Documentation
* `http://localhost:30003/` - locations OpenApi Documentation
* `http://localhost:30001/api/` - Base path for API
* `http://localhost:30000/` - Frontend ReactJS Application

#### Deployment Note
You may notice the odd port numbers being served to `localhost`. [By default, Kubernetes services are only exposed to one another in an internal network](https://kubernetes.io/docs/concepts/services-networking/service/). This means that `udaconnect-app` and `udaconnect-api` can talk to one another. For us to connect to the cluster as an "outsider", we need to a way to expose these services to `localhost`.

Connections to the Kubernetes services have been set up through a [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). (While we would use a technology like an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) to expose our Kubernetes services in deployment, a NodePort will suffice for development.)

