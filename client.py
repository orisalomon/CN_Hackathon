
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

        # print out client message
        print(f"{Fore.CYAN}{Style.BRIGHT}Client started, listening for offer requests...")

        self.client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client_udp.bind(('172.99.255.255', self.udpPort))


    def lookingForOffers(self):
        while True:
        ## connect to server
            data, addr = self.client_udp.recvfrom(self.bufferSize)
            magicCookie,messageType,serverPort = struct.unpack('>IBH',data)

            if hex(int(magicCookie)) != 0xabcddcba or hex(int(messageType)) != 0x2:
                continue

            return addr[0],serverPort

    def connectToServer(self,addr,serverPort):
        print(f"{Fore.CYAN}{Style.BRIGHT}Received offer from {addr}, attempting to connect...")

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 

        try:
            # print(serverPort)
            self.tcp_socket.connect((addr,serverPort))
            # self.tcp_socket.connect((socket.gethostname(),self.clientPort))
        except Exception as e:
            print(f"exception: {e}")
            return
        # self.tcp_socket = client_tcp
        return self.tcp_socket

    def gameMode(self, conn):
        ans = []

        def handleInput(conn):
            try:
                userInput = getch.getch()
                conn.send(userInput.encode())  # send client answer
                
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}exception: {e}")

        

        conn.send(self.name.encode()) # send group name


        question = conn.recv(self.bufferSize).decode()  # receive response
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{question}")  # show in terminal

        p = Process(target=handleInput,args=(conn,))
        try:
            p.start()

        except:
            print(f"{Fore.RED}{Style.BRIGHT}no answer from client!")

        serverResult = conn.recv(self.bufferSize).decode()  # receive response
        os.kill(p.pid,signal.SIGKILL)
        
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{serverResult}")            
        


client = Client() ## init server and TCP connection
while(True):
    try:
        addr,serverPort = client.lookingForOffers()
        conn = client.connectToServer(addr,serverPort)
        if not conn:
            client.tcp_socket = None
            continue
        client.gameMode(conn)
        # print out client message
        print(f"{Fore.CYAN}{Style.BRIGHT}Server disconnected, listening for offer requests...")
        client.tcp_socket = None
        # conn.close()  # close the connection
    except Exception as e:
        # print(f"{Fore.RED}{Style.BRIGHT}error has occured: {e}")
        client.tcp_socket = None
        continue
    

