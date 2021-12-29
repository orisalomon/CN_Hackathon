# Import socket module
import socket
import config 
import time              
import threading
import random
import struct
import stoppableThread
from scapy.all import get_if_addr
import select
# import bcolors
from colorama import Fore, Back, Style


class Server:

    def __init__(self):
        
        ## Server Details ##
        self.server_port = config.SERVER_PORT
        self.server_buffer_size = config.SERVER_BUFFER_SIZE
        self.host_name = get_if_addr('eth1')
        # self.host_name = socket.gethostname()
        # self.ip_address = socket.gethostbyname(self.host_name)
        self.udp_port = config.UDP_BROADCAST_PORT
        
        ### players ##
        self.client1 = None
        self.client2 = None
        # print out server message
        # print(f"Server started, listening on IP address {self.host_name}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Server started, listening on IP address {self.host_name}")
        # print(Style.RESET_ALL)

        # print(f"{bcolors.OKBLUE}Server started, listening on IP address {self.host_name}{bcolors.ENDC}")


        self.server_socket = socket.socket()  # get instance
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.server_socket.bind((self.host_name, self.server_port))  # bind host address and port together
        self.server_socket.bind(('', self.server_port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        self.server_socket.listen(2)
        

    def establishTCPServer(self):       
        ########################## TCP ################################


        def thread_function(socket):
            while not (self.client1 and self.client2): 
                conn, address = socket.accept()
                print(address)
                # if address[0] != "172.1.0.39":
                #     continue
                
                if(self.client1 is  None and self.client2 is None):
                    self.client1 = (conn,address)


                elif (self.client1 is not None and self.client2 is None):
                    self.client2 = (conn,address)
                

        t = threading.Thread(target=thread_function,args=(self.server_socket,))  # accept new connection
        t.start()


    def udpBroadcast(self):

        ########################## UDP ################################
        
        # Create a UDP socket object
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        # set broadcast mode
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        ## CREATE UDP PACKET ##
        udp_packet = struct.pack('>IbH', 0xabcddcba, 0x2, self.server_port)

        while not (server.client1 and server.client2): 
            # udp_socket.sendto(udp_packet,('<broadcast>', self.udp_port))
            split_host = self.host_name.split(".")
            addr_udp = f"{split_host[0]}.{split_host[1]}.255.255"
            udp_socket.sendto(udp_packet,(addr_udp, self.udp_port))
            time.sleep(1)
            
        ## close udp socket after found 2 players
        udp_socket.close()
            

    def handleAnswer(self):
        
        ans = []

        def threadAnswer(player_id,conn):
            try:
                clientAns = None
                clientAns = conn.recv(self.server_buffer_size).decode()
                if(clientAns is not None):
                    ans.append((clientAns,player_id))       
            except Exception as e:
                print(e)

        
        # self.client1[0].settimeout(10.0)
        # self.client2[0].settimeout(10.0)

        t0 = stoppableThread.StoppableThread(target=threadAnswer,args=(0,self.client1[0]))
        t1 = stoppableThread.StoppableThread(target=threadAnswer,args=(1,self.client2[0]))
        # run threads
        t0.start()
        t1.start()
        finish_time = time.time() + 10
        while(time.time() < finish_time):
            time.sleep(0.001) ## PATCH
            if(len(ans) > 0):
                t0.stop()
                t1.stop()
                return ans[0]
        t0.stop()
        t1.stop()
        
    def gameMode(self):
    ########### GAME MODE ################

        print("starting game in 10 seconds ...")

        time.sleep(3)
        # receive groups names
        name1 = self.client1[0].recv(self.server_buffer_size).decode()
        name2 = self.client2[0].recv(self.server_buffer_size).decode()

        number1 = random.randint(1,5)
        number2 = random.randint(1,4)
        operator = ["+","-"][random.randint(0,1)]
        if(operator == "+"):
            result = number1 + number2
        else:
            result = abs(number1 - number2)
        
        question = f"{number2 if number1<number2 else number1}{operator}{number1 if number1<number2 else number2}"
# {Fore.MAGENTA}{Style.BRIGHT}
# print(Style.RESET_ALL)
        message = \
        f"""
        Welcome to Quick Maths.
        Player 1: {name1}
        Player 2: {name2}
        ==
        Please answer the following question as fast as you can:
        How much is {question}?
        """
        self.client1[0].send(message.encode()) # ask question 
        self.client2[0].send(message.encode()) # ask question 
        answer = self.handleAnswer()
        drawMessage = f"""Game over!
        The correct answer was {result}!

        Game finished with a DRAW!
        """ 
        if(not answer): 
            # send draw message
            self.client1[0].send(drawMessage.encode())
            self.client2[0].send(drawMessage.encode()) 
            return
            
        try:
            answer_0 = int(answer[0])
        
        except:
            answer_0 = -1

        groupWinName = [name1,name2][answer[1]] if answer_0==result else [name1,name2][1-answer[1]]

        winMessage = f"""Game over!
            The correct answer was {result}!

            Congratulations to the winner: {groupWinName}
            """ 
        # send finish message to groups
        self.client1[0].send(winMessage.encode())
        self.client2[0].send(winMessage.encode()) 
        



server = Server() ## init server and TCP connection
while(True):
    try:
        server.establishTCPServer()
        server.udpBroadcast() # send udp broadcast messages for the clients to join the game
        server.gameMode() # handle game after found players

        # close clients TCP connections
        # server.client1[0].close()
        # server.client2[0].close()

        # remove groups from server
        server.client1 = None
        server.client2 = None

        # print out server message
        
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Game over, sending out offer requests...")
        # print(Style.RESET_ALL)
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}error has occured: {e}")
        server.client1 = None
        server.client2 = None
        continue
