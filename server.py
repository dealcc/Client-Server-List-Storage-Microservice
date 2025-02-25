import zmq
import pickle
import sqlite3
############################################ FUNCTION DEFINITIONS ############################################

# Function to connect to the database
def connect_db():
    return sqlite3.connect('data.db')




############################################
# This function creates a table in the database if it does not already exist.
#
# inputs : None
#
# outputs: None
###########################################
def create_table():
    # connect to the database
    with connect_db() as conn:
        cursor = conn.cursor() # create a cursor object to execute SQL queries
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id TEXT PRIMARY KEY,
                items TEXT
            )
        ''') # sql query to create a table with columns id and items
        conn.commit() # commit the transaction




############################################
# This function saves a list to the database with a unique ID.
#
# inputs : id: str - a unique identifier for the list
#          data_list: List - a list of items to save to the database
#
# outputs: None
###########################################
def save_list_to_db(id, data_list):
    # connect to the database
    with connect_db() as conn:
        cursor = conn.cursor() # create a cursor object to execute SQL queries
        items = pickle.dumps(data_list) # pickle.dumps() serializes the list for saving to the database
        cursor.execute('''
            INSERT INTO data (id, items) VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET items=excluded.items
        ''', (id, items)) # sql query to insert or update the data in the table
        conn.commit() # commit the transaction





############################################
# This function loads a list from the database using a unique ID.
#
# inputs : id: str - a unique identifier for the list
#
# outputs: List - a list of items loaded from the database
###########################################
def load_list_from_db(id):
    # connect to the database
    with connect_db() as conn:
        cursor = conn.cursor() # create a cursor object to execute SQL queries
        cursor.execute('SELECT items FROM data WHERE id = ?', (id,)) # sql query to select the items from the table
        row = cursor.fetchone() # fetches the first row from the result set

        # checks if the row exists
        if row:
            return pickle.loads(row[0]) # pickle.loads() deserializes the items from the database
        return None





############################################
# This function deletes a list from the database using a unique ID.
#
# inputs : id: str - a unique identifier for the list
#
# outputs: None
###########################################
def delete_list_from_db(id):
    # connect to the database
    with connect_db() as conn:
        cursor = conn.cursor() # create a cursor object to execute SQL queries
        cursor.execute('DELETE FROM data WHERE id = ?', (id,)) # sql query to delete the data from the table
        conn.commit() # commit the transaction




############################################ SERVER IMPLEMENTATION ############################################

# creating the zmq context and binding to the server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# create the table in the database (empty)
create_table()

# server loop to receive and respond to requests
while True:
    # receive the message from the client
    message = socket.recv()
    request = pickle.loads(message) # pickle.loads() deserializes the request dictionary

    print(f"Received request: {request}")

    # check the type of request and respond accordingly
    if request["type"] == "send_list":

        id = request["id"]
        data_list = request["data"]
        save_list_to_db(id, data_list) # save the list to the database
        response = {"status": "success", "message": "List received and saved."}

    elif request["type"] == "request_list":

        id = request["id"]
        data_list = load_list_from_db(id) # load the list from the database

        # check if the list exists
        if data_list is not None:
            response = {"status": "success", "data": data_list}
        else:
            response = {"status": "error", "message": "ID not found."}

    elif request["type"] == "delete_list":

        id = request["id"]
        delete_list_from_db(id) # delete the list from the database
        response = {"status": "success", "message": "List deleted."}

    else:
        response = {"status": "error", "message": "Invalid request type."}

    # send the response back to the client
    print(f"Sending response: {response}")
    socket.send(pickle.dumps(response)) # pickle.dumps() serializes the response dictionary for sending over the network