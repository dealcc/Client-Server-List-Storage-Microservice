# Client-Server-List-Storage-Microservice


## CREATING AND DELETING DATA 
 
To create data and send it to the server, refer to the client.py file, specifically the send_list(id, data_list) function  

The three lines contained are essential for properly sending the message, as the server is expecting a pickle serialized data list and a unique id through a zmq python request:


```
# dependencies: zmq and pickle

data_list = ["item1". "item2", "item3"]
id = "1234"

request = {"type": "send_list", "id": id, "data": data_list}
socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
# get the success response from server
response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
```
  
To edit an entry in the database, simply do the same method as above with the ID of the entry you would like to change and a new list and the server will automatically update the entry with that new list  
  
To delete an entry in the database, refer to the delete_list() function in client.py, it is essentially the same as send_list in its request but instead of the type being "send_list", it is now "delete_list" and with no "data" entry:

```
# dependencies: zmq and pickle
id = "1234"
request = {"type": "delete_list", "id": id} # define the request dictionary
socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
```
  
## REQUESTING AND RECEIVING DATA
  
To request for data, you first must know the unique id value of the list you would like to access. Requesting a list is the same 3 lines of code as the delete list code, except now the type of the request is "request_list":  

```
# dependencies: zmq and pickle
request = {"type": "request_list", "id": id}
socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
```

# UML DIAGRAM UTILIZING EXAMPLE CLIENT IMPLEMENTATION 
(![UML diagram of example client implementation](https://github.com/user-attachments/assets/56edc118-ae07-4481-869a-ca5f91a10238)

