
# Import socket module
import socket			

# print out client message
print("Client started, listening for offer requests...")

client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_udp.bind(("", 13117))

while True:
## connect to server
    data, addr = client_udp.recvfrom(1024)
    break
print(f"Received offer from {addr}, attempting to connect...")

client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM
) # TCP Socket

client_tcp.connect((addr[0],5000))

# receive data from the server and decoding to get the string.
# print (s.recv(1024).decode())

message = input(" -> ")  # take input

while message.lower().strip() != 'bye':
    client_tcp.send(message.encode())  # send message
    data = client_tcp.recv(1024).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal

    message = input(" -> ")  # again take input

client_tcp.close()  # close the connection


# # close the connection
# client_socket.close()



# # # Create a socket object
# client_socket = socket.socket()		

# # Define the port on which you want to connect
# port = 12345			

# # connect to the server on local computer
# client_socket.connect(('192.168.253.1', port))

# # receive data from the server and decoding to get the string.
# # print (s.recv(1024).decode())

# message = input(" -> ")  # take input

# while message.lower().strip() != 'bye':
#     client_socket.send(message.encode())  # send message
#     data = client_socket.recv(1024).decode()  # receive response

#     print('Received from server: ' + data)  # show in terminal

#     message = input(" -> ")  # again take input

# client_socket.close()  # close the connection


# # close the connection
# client_socket.close()


# print("Client started, listening for offer requests...")
# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# # Set broadcasting mode
# client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# client.bind(('', 13117))
