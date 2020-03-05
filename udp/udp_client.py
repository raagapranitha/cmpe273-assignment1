import socket
import os
import random
import sys
from time import sleep

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
#MESSAGE = "ping"
LOG = "CLIENT:"

def send(client_id=0):
    f_out=open("udp_client_out.txt","w")
    print(f'Starting client with ID: {client_id}')
    f_out.write(f'Starting client with ID: {client_id}\n')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        #.setblocking(True)
        f=open(os.curdir+"/upload.txt","r")
        print('Starting a file (upload.txt) upload...')
        f_out.write(f'Starting a file (upload.txt) upload...\n')
        header=random.randint(0,10000)
        for line in f.readlines():
            has_ack=False
            #print(LOG + f'Sending from client{client_id}: line={line.rstrip()} header={header}')
            s.sendto(f"{client_id}:{line}:{header}".encode(),(UDP_IP, UDP_PORT))
            send_counter=1
            while True:
                #print(LOG + "While loop started")
                try:
                    data, ip = s.recvfrom(BUFFER_SIZE)
                    sleep(0)
                except socket.timeout:
                    print("No data even after waiting for 1 sec resending packet")
                    f_out.write(f"No data even after waiting for 1 sec resending packet\n")
                    if send_counter<=3:
                        s.sendto(f"{client_id}:{line}:{header}".encode(),(UDP_IP, UDP_PORT))
                        send_counter+=1
                        continue
                    else:
                        print('Server not responding')
                        f_out.write(f'Server not responding\n')
                        exit()
                #print('LOG : Data received')
                recvd_data=(data.decode(encoding="utf-8").strip()).split(':')
                recvd_header=int(recvd_data[len(recvd_data)-1])
                if recvd_header==header:
                    has_ack=True   
                    print(f'CLIENT{client_id}:Got ACK from server with UID={recvd_header}')
                    f_out.write(f'CLIENT{client_id}:Got ACK from server with UID={recvd_header}\n')
                    break
            header+=1   
        print(f'Client{client_id}:File upload successfully completed')
        f_out.write(f'Client{client_id}:File upload successfully completed\n')
        f.close()
        f_out.flush()
        f_out.close()
        #exit()
    except:
        print('Closing socket')
        f_out.write(f'Closing socket')
                
send(sys.argv[1])