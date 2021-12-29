
# Import socket module
import socket	
# import stoppableThread
import config
import sys
import select
from scapy.all import get_if_addr
import getch
from colorama import Fore, Back, Style
import struct
import os
from multiprocessing import Process
import signal



class Client:
    
    def __init__(self):
        self.udpPort = config.UDP_BROADCAST_PORT
        self.clientPort = config.CLIENT_PORT
        self.serverAddr = None
        self.bufferSize = config.CLIENT_BUFFER_SIZE
        self.tcp_socket = None
        self.name = config.CLIENT_NAME
        # self.serverPort = None

        # print out client message
        print(f"{Fore.CYAN}{Style.BRIGHT}Client started, listening for offer requests...")

        self.client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_udp.bind(('', self.udpPort))


    def lookingForOffers(self):
        while True:
        ## connect to server
            data, addr = self.client_udp.recvfrom(self.bufferSize)
            # if addr[0] == "172.18.0.39":
            magicCookie,messageType,serverPort = struct.unpack('IbH',data)
            # if(serverPort != 2039):
            #     continue
            if(magicCookie == 0xabcddcba and messageType == 0x2):
                print(addr)
                break
        return addr[0],serverPort

    def connectToServer(self,addr,serverPort):
        print(f"{Fore.CYAN}{Style.BRIGHT}Received offer from {addr}, attempting to connect...")

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 
        # client_tcp = self.tcp_socket
        # self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        try:
            # print(serverPort)
            self.tcp_socket.connect((addr,serverPort))
            # self.tcp_socket.connect((socket.gethostname(),self.clientPort))
        except Exception as e:
            print(f"exception: {e}")
            return None
        # self.tcp_socket = client_tcp
        return self.tcp_socket

    def gameMode(self, conn):
        ans = []
        server_sent_message = False
        def handleInput(conn):
            try:
                # while len(select.select([sys.stdin.fileno()], [], [], None)[0]) > 0 and not server_sent_message:
                #     userInput = os.read(sys.stdin.fileno(), 1024)
                userInput = getch.getch()
                print(f"I clickted: {userInput}")
                conn.send(userInput.encode())  # send client answer
                
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}exception: {e}")

        

        conn.send(self.name.encode()) # send group name


        question = conn.recv(self.bufferSize).decode()  # receive response
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{question}")  # show in terminal


        # client_tcp.settimeout(10.0)
        p = Process(target=handleInput,args=(conn,))
        try:
            p.start()

        except:
            print(f"{Fore.RED}{Style.BRIGHT}no answer from client!")

        ## answer handling ##
        
        # readables, writeables, exceptions = select.select([self.tcp_socket,sys.stdin], [], [])
        # is_finished = False
        # while(not is_finished):
        #     for sock in readables:
        #         if sock == self.tcp_socket:
        #             serverResult = conn.recv(self.bufferSize).decode()  # receive response
        #             print(serverResult)
        #             is_finished = True
        #             break
            
        #         elif sock == sys.stdin:
        #             # message = getch.getch()
        #             message = sys.stdin.readline()
        #             conn.send(message.encode())
        serverResult = conn.recv(self.bufferSize).decode()  # receive response
        os.kill(p.pid,signal.SIGKILL)
        # p.kill()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{serverResult}")            
        


client = Client() ## init server and TCP connection
while(True):
    try:
        addr,serverPort = client.lookingForOffers()
        conn = client.connectToServer(addr,serverPort)
        if not conn:
            continue
        client.gameMode(conn)
        # print out client message
        print(f"{Fore.CYAN}{Style.BRIGHT}Server disconnected, listening for offer requests...")
        # conn.close()  # close the connection
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}error has occured: {e}")
        client.tcp_socket = None
        continue
    

