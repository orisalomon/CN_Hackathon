# Import socket module
import socket
import config 
import time              
import threading

host = socket.gethostbyname(socket.gethostname())

########################## UDP ################################

# Create a UDP socket object
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP Socket   
# set broadcast mode
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def thread_function(func, data, to_send):
    while True:
        func(data,to_send)
        time.sleep(1)
    

# print out server message
print(f"Server started, listening on IP address {host}")

is_full = False
c_addr_lst = []
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
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))
while True:
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = conn.recv(1024).decode()
    if not data:
        # if data is not received break
        break
    print("from connected user: " + str(data))
    data = input(' -> ')
    conn.send(data.encode())  # send data to the client

conn.close()  # close the connection
