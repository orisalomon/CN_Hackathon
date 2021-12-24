
# Import socket module
import socket	
import stoppableThread

def handleInput(conn):
    try:
        client_ans = input().encode()
        conn.send(client_ans)  # send client answer
    except:
        pass

# print out client message
print("Client started, listening for offer requests...")

client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
# client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

client_tcp.send(input().encode())  # send group name

question = client_tcp.recv(1024).decode()  # receive response
print(question)  # show in terminal


# client_tcp.settimeout(10.0)
t = stoppableThread.StoppableThread(target=handleInput,args=(client_tcp,))
try:
    s = t.start()

except:
    print("no answer from client!")


serverResult = client_tcp.recv(1024).decode()  # receive response
t.stop()
print(serverResult)

client_tcp.close()  # close the connection




