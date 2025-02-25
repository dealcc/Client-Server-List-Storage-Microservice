# Client-Server-List-Storage-Microservice

## SETUP
To be able to communicate with the server, the user needs to create a zmq socket and connect to the server via port. Currently, the server is setup for port 5555.  
The code that is needed before any of the other code that will be described in this readme must be:  
```
# dependencies: zmq and pickle
# creating the zmq context and connecting to the server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
```

## CREATING AND DELETING DATA 
 
To create data and send it to the server you simply create the list of data and a unique id for said data, then create a request with those two fields and serialize them to send over the network, then send use the socket you created to send it over the network. Refer to the code example below:    


```
data_list = ["item1". "item2", "item3"]
id = "1234"

request = {"type": "send_list", "id": id, "data": data_list}
socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
# get the success response from server
response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
```
  
To edit an entry in the database, simply do the same method as above with the ID of the entry you would like to change and a new list and the server will automatically update the entry with that new list  
  
To delete an entry in the database, it is essentially the same as send_list in its request but instead of the type being "send_list", it is now "delete_list" and with no "data" entry:

```
id = "1234"
request = {"type": "delete_list", "id": id} # define the request dictionary
socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
```
  
## REQUESTING AND RECEIVING DATA
  
To request and receive data, you first must know the unique ID value of the list you would like to access. Requesting and receiving a list is the same 3 lines of code as the delete list code, except now the type of the request is "request_list":  

```
request = {"type": "request_list", "id": id}
socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
```
The "response" variable in this code should contain the data list that was requested or an error message saying that the ID does not exist in the database.

# UML DIAGRAM UTILIZING EXAMPLE CLIENT IMPLEMENTATION 
(![UML diagram of example client implementation](https://github.com/user-attachments/assets/a537bd00-4541-4f7e-b0f8-41f2316e1b30))

