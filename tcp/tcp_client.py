import socket
import time
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"
sleep_sec=int(sys.argv[2])
NO_OF_MESSAGES = int(sys.argv[3])



def send(id=0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f_client = open('tcp_client_out.txt','w')
    try:
        s.connect((TCP_IP, TCP_PORT))
    except:
        print('Could not connect to server')
    print('Connected to server')
    f_client.write(f'Connected to server')
    i = 0
    while True:
        if i > NO_OF_MESSAGES:
            break
        send_message = f'{id} : ping '
        s.send(send_message.encode())
        time.sleep(sleep_sec)
        try:
            data = s.recv(1024)
        except:
            print('No data received')
        recvd_data = data.decode()
        print(f'Received: {recvd_data}')
        f_client.write(f'Received: {recvd_data}\n')
        i += 1
    f_client.close()    
    s.close()

send(sys.argv[1])
