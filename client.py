import socket
import time
import matplotlib.pyplot as plt

# maxseqsentSize is total number of sent seq (include retransmissions)
maxseqSentSize = 10000000

expectedRecvNum = 0
next_seq = 0
window_size = 1
actualRecvNum = 0
window_size_time = []
window_size_list = []
dict = {}
acutalTotalSeq = 0
acutalTotalACk = 0

def printclientIP():
    # get sender ip address
    clientIP = socket.gethostbyname(socket.gethostname()) 
    # print sender ip address
    print("Sender IP address is : " + clientIP) 
printclientIP()

# initial funtion: try to connect with Server and proof success
def initial():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # For the convenience of testing, we use the ip address of local hosts. If using two separate machines, then change the ip address. 
    client.connect(('127.0.0.1', 1234))
    # send the server an initial string "network"
    client.send(bytes('network',"utf-8"))
    msg = client.recv(1024)
    print(msg.decode("utf-8"))
initial()

# Timer to draw the graphs 
start_time = time.time()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# For the convenience of testing, we use the ip address of local hosts. If using two separate machines, then change the ip address. 
client.connect(('127.0.0.1', 1234))
while True:
    for i in range(window_size):
        # send seq num to server
        client.send(bytes((str(next_seq)+ "\n") ,"utf-8")) 
        print("Sending " , str(next_seq) + "   total sent packet: " , acutalTotalSeq) 
        # To record the number of retransmissions for the seq num
        if next_seq in dict.keys():
            dict[next_seq] = dict[next_seq] + 1
        else:
            dict[next_seq] = 1 
        next_seq += 1
        acutalTotalSeq += 1
        if next_seq >= 65536: # maximum sequence number should be limited to 2^16
            next_seq = 1
            expectedRecvNum = 1
    if acutalTotalSeq >= maxseqSentSize:
        break

    data = client.recv(4096)
    num_str_List = data.decode().split('\n')
    for i in range(len(num_str_List)):
        num_str = num_str_List[i]
        if num_str:
            if len(num_str.split(' ')) > 1: 
                actualRecvNum = int(num_str.split(' ')[1])
                if actualRecvNum == expectedRecvNum:
                    expectedRecvNum += 1
                    acutalTotalACk += 1
                    if expectedRecvNum == next_seq:
                        # For graphs 1 use
                        window_size_time.append(time.time() - start_time) 
                        window_size_list.append(window_size) 
                        window_size *= 2
                else:
                    next_seq = expectedRecvNum
                    if window_size / 2 != 0:
                        window_size_time.append(time.time() - start_time)
                        window_size_list.append(window_size)
                        window_size = (int)(window_size / 2)
                    break

# To record and print the number of retransmissions for the seq num
def retransTime():
    retrans1time = []
    retrans2time = []
    retrans3time = []
    retrans4time = []
    retrans5time = []
    retrans6time = []

    for key in dict.keys():
        if (dict[key] == 2):
            retrans1time.append(key)
        if (dict[key] == 3):
            retrans2time.append(key)
        if (dict[key] == 4):
            retrans3time.append(key)
        if (dict[key] == 5):
            retrans4time.append(key)
        if (dict[key] == 6):
            retrans5time.append(key)
        if (dict[key] == 7):
            retrans6time.append(key)

    print("retrans  1 time: ", retrans1time)
    print("retrans  2 time: ", retrans2time)
    print("retrans  3 time: ", retrans3time)
    print("retrans  4 time: ", retrans4time)
    print("retrans  5 time: ", retrans5time)
    print("retrans  6 time: ", retrans6time)
    print("retrans  1 time size ", len(retrans1time))
    print("retrans  2 time size ", len(retrans2time))
    print("retrans  3 time size ", len(retrans3time))
    print("retrans  4 time size ", len(retrans4time))
    print("retrans  5 time size ", len(retrans5time))
    print("retrans  6 time size ", len(retrans6time))
retransTime()

# draw graphs 1
def drawWinSize():
    plt.plot(window_size_time, window_size_list)
    plt.xlabel('time')
    plt.ylabel('winSize')
    plt.show()
    plt.savefig('winSize_time2.png')
drawWinSize()

client.close()
