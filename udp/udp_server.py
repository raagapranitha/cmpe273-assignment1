import socket
from time import sleep
import os

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
#MESSAGE = "pong"
LOG = "SERVER:"
id_headers={}

def send_ack(socket, client_id, header, ip):
    #print(LOG + f'Sending from server to client{client_id}: header={header}')
    socket.sendto(f'{id_headers[client_id]}:{header}'.encode(),ip)


def listen_forever():
    global id_headers
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    s.bind(("", UDP_PORT))
    with open('udp_server_out.txt','a') as f_server:
        print(LOG + "Server up and listening on port " + str(UDP_PORT))
        line=LOG + "Server up and listening on port " + str(UDP_PORT) +'\n'
        f_server.write(line)
        i=0
        print('Accepting file upload...')
        f_server.write(f'Accepting file upload...\n')    
        try:
            while True:
                # get the data sent to us
                try:
                    data, ip = s.recvfrom(BUFFER_SIZE)
                except socket.timeout:
                    print('No data ')
                    break
                recvd_data=(data.decode(encoding="utf-8").strip()).split(':')
                client_id=int(recvd_data[0])
                curr_header=int(recvd_data[len(recvd_data)-1])
                i+=1
                prev_header = id_headers.get(client_id, curr_header)
                if curr_header == prev_header or curr_header == prev_header+1:
                    # when curr_header == prev_header, possibly the client did not receive the ACK, resend the ACK
                    # when curr_header == prev_header+1, update the prev_header with curr_header and send ACK
                    id_headers.update({client_id:curr_header})
                    send_ack(s, client_id, curr_header, ip)         
                else:
                    #missed packet, wait for client to resnd the packet
                    print(LOG + "missed packet")
        except KeyboardInterrupt:
            print("Key Press interrupt")
            #line='Key Press interrupt \n'
            f_server.write(f'Key Press interrupt \n')
        print('SERVER:Upload successfully completed.')
        f_server.write(f'SERVER:Upload successfully completed.\n')
        f_server.flush()
        f_server.close()
        return False
listen_forever()