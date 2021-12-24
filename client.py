
# Import socket module
import socket	
import stoppableThread
import config


class Client:

    def __init__(self):
        self.udpPort = config.UDP_BROADCAST_PORT
        self.serverPort = config.SERVER_PORT
        self.serverAddr = None
        self.bufferSize = config.CLIENT_BUFFER_SIZE
        
        # print out client message
        print("Client started, listening for offer requests...")

    def lookingForOffers(self):

        client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_udp.bind(("", self.udpPort))

        while True:
        ## connect to server
            data, addr = client_udp.recvfrom(self.bufferSize)
            break
        return data, addr

    def connectToServer(self, data, addr):
        print(f"Received offer from {addr[0]}, attempting to connect...")

        client_tcp = socket.socket() # TCP Socket
        try:
            client_tcp.connect((socket.gethostname(),self.serverPort))
        except:
            return None

        return client_tcp

    def gameMode(self, conn):
        def handleInput(conn):
            try:
                client_ans = input().encode()
                conn.send(client_ans)  # send client answer
            except:
                pass
        print("send name")
        conn.send(input().encode())  # send group name

        question = conn.recv(self.bufferSize).decode()  # receive response
        print(question)  # show in terminal


        # client_tcp.settimeout(10.0)
        t = stoppableThread.StoppableThread(target=handleInput,args=(conn,))
        try:
            s = t.start()

        except:
            print("no answer from client!")


        serverResult = conn.recv(self.bufferSize).decode()  # receive response
        t.stop()
        print(serverResult)


client = Client() ## init server and TCP connection
while(True):
    data, addr = client.lookingForOffers()
    conn = client.connectToServer(data, addr)
    if not conn:
        continue
    client.gameMode(conn)
    # print out client message
    print("Server disconnected, listening for offer requests...")
    conn.close()  # close the connection

