#import client as client
from itertools import permutations
import socket

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


def send(msg, client):
    try:
        # print(msg)
        msg_length = str(len(msg))
        padding = " "*(HEADER-len(msg_length))
        msg_length += padding
        msg_length = msg_length.encode(FORMAT)

        client.send(msg_length)
        #print('Sent message length')

        client.send(msg.encode(FORMAT))

        #print('sent message')

    except:
        print(f"Error in sending message to server")


def receive(client):
    try:
        msg_length = int(client.recv(HEADER).decode(FORMAT))
        msg = client.recv(msg_length)

        return msg.decode(FORMAT)

    except:
        print('Error in receiving message from server')
        return "Not Found\n"


def test1():

    command = f"set fname 5\r\nVamsi\r\n"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(command, client)

    resp = receive(client)

    send("Disconnect", client)
    receive(client)

    if resp == "Stored\r\n":
        print('Pass')
    else:
        print('fail')


test1()


def multirequestTest():
    #temp_map = dict()
    keys = ["fname", "lname"]

    set_commands = []
    fnames = list(map(lambda x: ''.join(x), permutations("VVamsi")))
    lnames = list(map(lambda x: ''.join(x), permutations("Bushan")))

    for i in range(250):
        set_commands.append(f"set fname {len(fnames[i])}\r\n{fnames[i]}\r\n")

    for i in range(250):
        set_commands.append(f"set lname {len(lnames[i])}\r\n{lnames[i]}\r\n")
    #commands = ["set"]*500+["get"]*500

    s = 0
    for i in range(500):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        send(set_commands[i], client)

        resp = receive(client)

        send("Disconnect", client)
        receive(client)

        if resp == "Stored\r\n":
            s += 1

    if s == 500:
        print("Pass")
    else:
        print("Fail")


multirequestTest()
