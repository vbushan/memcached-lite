import socket
import memcacheAPI
import threading


class Memcached:

    def __init__(self, HEADER, PORT, SERVER_IP, FORMAT):

        self.HEADER = HEADER
        self.PORT = PORT
        self.SERVER_IP = SERVER_IP
        self.ADDR = (self.SERVER_IP, PORT)
        self.FORMAT = FORMAT
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.SERVER.bind(self.ADDR)

    def listen(self):
        self.SERVER.listen(1)

    def accept(self):
        return self.SERVER.accept()

    def commandHandler(self, cmd, lock):
        print('Parsing command')
        resp = ""
        try:
            print('In command handler')

            #cmd = cmd.decode(self.FORMAT)

            cmd = cmd.split("\r\n")

            print(cmd)

            command = cmd[0].split(" ")

            if command[0] == "set":

                key = command[1]
                bytes = int(command[2])

                value = cmd[1]
                print(value)
                resp = memcacheAPI.set(key, value, bytes, lock)

            elif command[0] == 'get':
                key = command[1]

                print('Get Key', key)
                resp = memcacheAPI.get(key)

            return resp
        except:
            print("Error occured!")

            return 'Error Occured'

    def send(self, conn, msg, addr):
        print(f'Sending response to {addr}. Response- {msg}')
        try:
            msg_length = str(len(msg))
            padding = " "*(self.HEADER-len(msg_length))

            msg_length += padding
            msg_length = msg_length.encode(self.FORMAT)

            #print('Sending Message Length')
            conn.send(msg_length)
            #print('Sent Message Length')

            #print('Sending Message')
            conn.send(msg.encode(self.FORMAT))
            #print('Sent Message')

        except:
            print(f'Error occured in sending message to {addr}')

    def receive(self, conn, addr):

        print(f'Receiving Message from {addr}')
        try:
            msg_length = int(conn.recv(self.HEADER).decode(self.FORMAT))

            #print(f'Received message length from {addr}. Length= {msg_length}')

            msg = conn.recv(msg_length).decode(self.FORMAT)
            #print('Message received', msg)
            print(f'Received message from {addr}. Message- {msg}')
            return msg

        except:
            print(f"Error occured in receiving message from {addr}")

    def serveClient(self, conn=None, addr=None, lock=None):
        try:
            while True:

                command = self.receive(conn, addr)
                if command == "Disconnect":
                    break
                response = self.commandHandler(command, lock)

                self.send(conn, response, addr)

            self.send(conn, "Disconnected", addr)
        except Exception as e:
            # print(e.message)
            print(f'Error Occurred in serving client {addr}')

        finally:
            conn.close()


if __name__ == "__main__":

    # Server configuration

    HEADER = 1024
    PORT = 5050
    SERVER_IP = socket.gethostbyname(socket.gethostname())
    FORMAT = 'utf-8'

    # Create an instance of memcache

    memcD_server = Memcached(HEADER, PORT, SERVER_IP, FORMAT)
    memcD_server.bind()

    # Start the server

    print("Preparing server to listen...")

    memcD_server.listen()

    print(f"Server is listening on {memcD_server.SERVER_IP}")

    while True:

        connSocket, addr = memcD_server.accept()

        print(f"Established connection with {addr}")

        thread = threading.Thread(
            target=memcD_server.serveClient, args=(connSocket, addr, threading.Lock()))
        thread.start()
        # thread.join()

        #print(f"Finished serving- {addr}")
