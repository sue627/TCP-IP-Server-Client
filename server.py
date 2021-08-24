import socket
import time
import matplotlib.pyplot as plt
import random

# maxACKSize is total number of ACK numbers
maxACKSize = 10000000

num_drop_list = []
num_drop_time = []
num_drop_list.append(0)
num_drop_time.append(0)

seq_receive_num_list = []
seq_receive_time = []

received_packet = 0
client_sent_packet = 0
expectedNum = 0
missing_package = 0

#should_miss funtion: randomly drop 1% probability for the sequence numbers
def should_miss():
	return random.randint(1, 100) == 1

def printServerIP():	
	# get receiver ip address
	serverIP = socket.gethostbyname(socket.gethostname()) 
	# print receiver ip address
	print("Receiver IP address is : " + serverIP) 
printServerIP()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# For the convenience of testing, we use the ip address of local hosts. If using two separate machines, then change the ip address. 
serv.bind(('0.0.0.0', 1234))
serv.listen()
print(f"waiting for connection...")

while True:
	clientsocket, address = serv.accept()
	while True:
		msg = clientsocket.recv(1024)
		print(msg.decode())
		# send the client success msg
		clientsocket.send(bytes("Success " + msg.decode(),"utf-8"))
		while True:
			clientsocket, address = serv.accept()
			start_time = time.time()
			while True:
				try:
					data = clientsocket.recv(4096)
					if not data: break
					for num_str in data.decode().split('\n'):
						if num_str:
							client_sent_packet += 1
							if should_miss():   
								missing_package += 1
								#For graphs 3 use
								num_drop_list.append(int(num_str)) 
								num_drop_time.append(time.time() - start_time) 
								continue
							actualNum = int(num_str)
							# Maximum sequence number should be limited to 2^16
							if actualNum == 1 and expectedNum >= 65536: 
								expectedNum = 1
							if actualNum == expectedNum:
								# Server respond to the client with the corresponding “ACK numbers”.
								clientsocket.send(bytes("ACK " + str(actualNum) + "\n", "utf-8")) 
								expectedNum += 1
								#For graphs 2 use
								seq_receive_num_list.append(expectedNum) 
								seq_receive_time.append(time.time() - start_time) 
								received_packet += 1
								print("received and sent ACK " + str(actualNum))
							else:
								# Server respond to the client with the corresponding “ACK numbers”.
								clientsocket.send(bytes("ACK " + str(actualNum) + "\n", "utf-8")) 
						if client_sent_packet == maxACKSize:
							print("Num of packets sent: " + str(client_sent_packet))
							print("Num of packets received: " + str(received_packet))
							print("Good-put: " + str(float(received_packet / client_sent_packet)))

							# draw graphs 2
							plt.plot(seq_receive_time, seq_receive_num_list)
							plt.xlabel('time')
							plt.ylabel('num seq recv')
							plt.show()

							# draw graphs 3
							plt.plot(num_drop_time, num_drop_list, 'ro')
							plt.xlabel('time')
							plt.ylabel('num seq drop')
							plt.show()
							break
						
				except ConnectionResetError:
					print("One client connection closed")
					break
			break
		print("Waiting for new connection...")
		break

	
	


        



