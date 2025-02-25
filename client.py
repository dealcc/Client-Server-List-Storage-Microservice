import zmq
import pickle

# creating the zmq context and connecting to the server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")



############################################ CLIENT FUNCTIONS ############################################

# defining the functions to send, request, and delete lists



############################################
# send_list(id: Int , data_list: List)
# this function sends a list to the server with a unique ID and a list of items
#
# inputs : id: Int - a unique identifier for the list
#          data_list: List - a list of items to send to the server 
#
# outputs: None
############################################
def send_list(id, data_list):
    request = {"type": "send_list", "id": id, "data": data_list}
    socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
    response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
    print(response)





############################################
# request_list(id: Int)
# this function requests a list from the server using a unique ID
#
# inputs : id: Int - a unique identifier for the list
#
# outputs: None
############################################
def request_list(id):
    request = {"type": "request_list", "id": id}
    socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
    response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary

    # checks for successfull entry
    if response["status"] == "success":
        data_list = response["data"]
        print("Received list:", data_list)
    else:
        print(response["message"])




############################################
# delete_list(id: Int)
# this function deletes a list from the server using a unique ID
#
# inputs : id: Int - a unique identifier for the list
#
# outputs: None
############################################
def delete_list(id):
    request = {"type": "delete_list", "id": id} # define the request dictionary
    socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
    response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
    print(response)




############################################ CLIENT USAGE ############################################

# TEST USAGE:
# Send a list to the server with a unique ID
send_list("123", ["item1", "item2", "item3"])

# Request the list from the server using the unique ID
request_list("123")

# Delete the list from the server using the unique ID
delete_list("123")

# Try to request the list again to confirm deletion
request_list("123")