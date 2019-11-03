import socket
from _thread import *
import sys
import run

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5556

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"

#### initializeing parameters
bid = ["0:0,0", "1:0,0"] # initial bids
##########################

def threaded_client(conn):
    global currentId, bid
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                #### reply is the decoded msg you received
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])

                #### pos is what is being passed around ## ie the info
                bid[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                #### you definitely have to change pos
                reply = bid[nid][:]
                ###### 

                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))

'''
each client run its own game and update its para according 
to the bid that has been passed ?
'''
