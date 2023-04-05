# location consumer

This is an application that waits for a message to be posted to the 'locations' kafka mailbox.
Then processes the 'locations' message by writing it to the database.

## Run

To run this application there are 2 steps required:

Go to the deployment directory and execute `kubectl apply -f location-consumer.yaml`