
import socket
import threading
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
class ThreadedServer(object):
    def __init__(self):
        #self.host = host
        #self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((TCP_IP,TCP_PORT ))
        print('TCP server up and running')

    def listen(self):
        self.sock.listen(5)
        while True:
            try:
                client, address = self.sock.accept()
            except:
                print("Could not accept client socket")    
            #client.settimeout(60)
            print('Connected to client')
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024   
        f=open('tcp_server_out.txt','w')      
        while True:
            try:
                data = client.recv(size)
                if data:
                    recvd_data=(data.decode())
                    # Set the response to echo back the recieved data 
                    print(f'Received Data: {recvd_data}')
                    f.write(f'Received Data: {recvd_data}\n')
                    response = "pong"
                    client.send(response.encode())
                else:
                    raise error('Client disconnected')
            except:
                #print('No data received')
                client.close()
                f.close()
                return False

if __name__ == "__main__":

    ThreadedServer().listen()