# Import socket module
import socket
import config 
import time              
import threading
import random


def gameMode(conn1,conn2=None):
########### GAME MODE ################

    # ask for the group names
    print("trying to send message")
    conn1.send("Server Message: Please send your team's name. ".encode())  # send welcoming message to the client1
    # conn2.send("Server Message: Please send your team's name. ".encode())  # send welcoming message to the client2

    # receive data stream. it won't accept data packet greater than 1024 bytes
    name1 = conn1.recv(1024).decode()
    # name2 = conn2.recv(1024).decode()
    # if not name1 or name2:
    if not name1:
        # if data is not received break
        return

    number1 = random.randint(1,5)
    number2 = random.randint(1,4)
    operator = ["+","-"][random.randint(0,1)]
    
    question = f"{number2 if number1<number2 else number1}{operator}{number1 if number1<number2 else number2}"

    message = \
    f"""
    Welcome to Quick Maths.
    Player 1: {name1}
    Player 2: NULL
    ==
    Please answer the following question as fast as you can:
    How much is {question}?
    """
    conn1.send(message.encode()) # ask question 

    # print("from connected user: " + str(data))
    # data = input(' -> ')
    # conn1.send(data.encode())  # send data to the client
    # conn2.send(data.encode())  # send data to the client
    
    answer = conn1.recv(1024).decode()
    print(f"recieved from client: {answer}")

    conn1.close()  # close the connection
# conn2.close()  # close the connection


def waitingForClient():
    have_2_clients = False
    def thread_function(func, data, to_send):
        while not have_2_clients: 
            func(data,to_send)
            time.sleep(1)
        
    ########################## UDP ################################
    # Create a UDP socket object
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP Socket   
    # set broadcast mode
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    host = socket.gethostbyname(socket.gethostname())
    # print out server message
    print(f"Server started, listening on IP address {host}")

    
    ########### BROADCAST #################

    string_to_send = b"connect to my server at IP: " + socket.gethostbyname(socket.gethostname()).encode() + b"Port: 5000" 
    # udp_socket.sendto(b"connect to my server at IP: " + socket.gethostbyname(socket.gethostname()).encode() + b"Port: 5000" , ('<broadcast>', 13117))

    udp_thread = threading.Thread(target=thread_function, args=(udp_socket.sendto,string_to_send,('<broadcast>', 13117),))
    udp_thread.start()

             
    ########################## TCP ################################

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    clients_lst = []
    conn1, address1 = server_socket.accept()  # accept new connection
    # conn2, address2 = server_socket.accept()  # accept new connection

    # stop boradcasting UDP
    have_2_clients = True

    clients_lst.append((conn1,address1))
    # clients_lst.append((conn2,address2))
    print("Connection from: " + str(address1))
    # print("Connection from: " + str(address2))

    return conn1,None


conn1,conn2 = waitingForClient()
time.sleep(3)
gameMode(conn1,conn2)