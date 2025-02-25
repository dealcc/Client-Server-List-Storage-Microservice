import zmq
import pickle

# creating the zmq context and connecting to the server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")



############################################ CLIENT FUNCTIONS ############################################

# defining the functions to send, request, and delete lists



############################################
# send_list(id: str , data_list: List)
# this function sends a list to the server with a unique ID and a list of items
#
# inputs : id: str - a unique identifier for the list
#          data_list: List - a list of items to send to the server 
#
# outputs: None
############################################
def send_list(id, data_list):
    request = {"type": "send_list", "id": id, "data": data_list}
    print(f"Sending Request: {request}")
    socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
    response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
    print(f"Response Acknowledged: {response}")





############################################
# request_list(id: str)
# this function requests a list from the server using a unique ID
#
# inputs : id: str - a unique identifier for the list
#
# outputs: None
############################################
def request_list(id):
    request = {"type": "request_list", "id": id}
    print(f"Sending Request: {request}")
    socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
    response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary

    # checks for successfull entry
    if response["status"] == "success":
        print(f"Response Acknowledged: {response}")
        data_list = response["data"]
        return data_list
    else:
        print(f"Error in Response: {response}")
        return response["message"]




############################################
# delete_list(id: str)
# this function deletes a list from the server using a unique ID
#
# inputs : id: str - a unique identifier for the list
#
# outputs: None
############################################
def delete_list(id):
    request = {"type": "delete_list", "id": id} # define the request dictionary
    print(f"Sending Request: {request}")
    socket.send(pickle.dumps(request)) # pickle.dumps() serializes the request dictionary for sending over the network
    response = pickle.loads(socket.recv()) # pickle.loads() deserializes the response dictionary
    print(f"Response Acknowledged: {response}")




############################################ CLIENT USAGE ############################################

# TEST USAGE:
# Send a list to the server with a unique ID
send_list("123", ["item1", "item2", "item3"])

# Request the list from the server using the unique ID
data = request_list("123")

# Delete the list from the server using the unique ID
delete_list("123")

# Try to request the list again to confirm deletion
data = request_list("123")