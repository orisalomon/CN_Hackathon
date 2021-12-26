
# Import socket module
import socket	
import stoppableThread
import config
import sys
import select



class Client:
    
    def __init__(self):
        self.udpPort = config.UDP_BROADCAST_PORT
        self.serverPort = config.SERVER_PORT
        self.serverAddr = None
        self.bufferSize = config.CLIENT_BUFFER_SIZE
        self.tcp_socket = None

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

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 
        # client_tcp = self.tcp_socket
        try:
            self.tcp_socket.connect((socket.gethostname(),self.serverPort))
        except:
            return None
        # self.tcp_socket = client_tcp
        return self.tcp_socket

    def gameMode(self, conn):

        # def handleInput(conn):
        #     try:
        #         userInput = input().encode()
        #         conn.send(userInput)  # send client answer
                
        #     except:
        #         print('timed out!')

        

        conn.send(input().encode()) # send group name

        question = conn.recv(self.bufferSize).decode()  # receive response
        print(question)  # show in terminal


        # # client_tcp.settimeout(10.0)
        # t = stoppableThread.StoppableThread(target=handleInput,args=(conn,))
        # try:
        #     t.start()

        # except:
        #     print("no answer from client!")

        ## answer handling ##

        readables, writeables, exceptions = select.select([self.tcp_socket], [], [],10)
        while(True):
            for sock in readables:
                print("Error 1")
                if sock == self.tcp_socket:
                    print("Error 2")
                    serverResult = conn.recv(self.bufferSize).decode()  # receive response
                    print(serverResult)
                    break
            
                elif sock == sys.stdin:
                    print("Error 3")
                    message = sys.stdin.readline() 
                    conn.send(message.encode())
                    break
        # t.stop()
        


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
    

