
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
print(f"Received offer from {addr[0]}, attempting to connect...")

client_tcp = socket.socket() # TCP Socket
client_tcp.connect((socket.gethostname(),5000))

# receive data from the server and decoding to get the string.
# print (s.recv(1024).decode())

message = input(" -> ")  # take input

while message.lower().strip() != 'bye':
    client_tcp.send(message.encode())  # send message
    data = client_tcp.recv(1024).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal

    message = input(" -> ")  # again take input

client_tcp.close()  # close the connection

