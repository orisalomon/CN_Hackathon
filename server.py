# Import socket module
import socket
import config 
import time              

# import threading

# def set_interval(func,data,to_send, sec):
#     def func_wrapper(data,to_send):
#         set_interval(func,data,to_send, sec)
#         func(data,to_send)
#         print("Broadcast sent!")
#     t = threading.Timer(sec, lambda: func_wrapper(data,to_send))
#     t.start()
#     return t


host = socket.gethostbyname(socket.gethostname())

# Create a UDP socket object
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP Socket   


########## TCP bind #############
# create server tcp socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM
) # TCP Socket

# Get local machine name
port = config.SERVER_PORT                
# Reserve a port for your service.

tcp_socket.bind((host, port))        
# Bind to the port

# maximum of 2 clients
tcp_socket.listen(2)                 


###############################################
# set broadcast mode
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

### Prints Server started ###
# host = socket.gethostname() 

# print out server message
print(f"Server started, listening on IP address {host}")

is_full = False
c_addr_lst = []
########### BROADCAST #################

string_to_send = b"connect to my server at IP: " + socket.gethostbyname(socket.gethostname()).encode() + b"Port: 5000" 
# udp_socket.sendto(b"connect to my server at IP: " + socket.gethostbyname(socket.gethostname()).encode() + b"Port: 5000" , ('<broadcast>', 13117))

set_interval(udp_socket.sendto,string_to_send,('<broadcast>', 13117),1)

# time.sleep(1)


# Establish connection with client.
c, addr = tcp_socket.accept()     

# Output the message and Close the connection
print ('Got connection from', addr)
c.send('Thank you for connecting'.encode())
c_addr_lst.append(c,addr)

for i in range(len(c_addr_lst)):
    c_addr_lst[i][0].send("hello client ".encode() + i.tobytes(2,'big'))
        


c.close()                

# print(f"Server started, listening on IP address {socket.gethostbyname(socket.gethostname())}")

