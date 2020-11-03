import socket

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
# SERVER = "192.168.56.1"
# SERVER = "127.0.1.1"
# SERVER = "129.79.247.5"
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)
ADDR = (SERVER, PORT)
# print(ADDR)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
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


def receive():
    try:
        msg_length = int(client.recv(HEADER).decode(FORMAT))
        msg = client.recv(msg_length)

        return msg.decode(FORMAT)

    except:
        print('Error in receiving message from server')
        return "Not Found\n"


def commandHandler():
    user_inp = input().split(" ")

    command = None

    if user_inp[0] == "set":
        command = "set"

    elif user_inp[0] == "get":
        command = "get"

    elif user_inp[0] == "Disconnect":
        command = "Disconnect"

    else:
        raise Exception('Invalid command')

    # print('Input Command', command)
    if command == 'set':

        set_command = ' '.join(user_inp)
        set_data = input()

        msg = set_command+"\r\n"+set_data+"\r\n"

    elif command == 'get':
        get_command = ' '.join(user_inp)

        msg = get_command+"\r\n"

    else:
        msg = command

    return msg


if __name__ == "__main__":
    try:

        while True:
            msg = commandHandler()
            if msg:
                send(msg)
                resp = receive()
                print(resp)

                if resp == 'Disconnected':
                    break

    except Exception as e:
        print(e)
