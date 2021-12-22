
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

insert_name = client_tcp.recv(1024).decode()  # receive response
print(insert_name)

client_tcp.send(input().encode())  # send message

question = client_tcp.recv(1024).decode()  # receive response
print(question)  # show in terminal

client_tcp.send(input().encode())  # send message

client_tcp.close()  # close the connection

