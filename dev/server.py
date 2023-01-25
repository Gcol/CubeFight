import socket
from config import HOST, PORT

class Server(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        param_server = (self.hostname, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((param_server))
        self.socket.listen()
        print (f'Serveur Running on {param_server}')

        conn = None
        try:
            conn, address = self.socket.accept()
            print(f'New Connecntio by {address}')
            while True:
                data = conn.recv(1024)
                print(data.decode('utf-8'))
                conn.send('Tout es bon'.encode('utf-8'))

        except:
            if conn:
                conn.close()
            self.socket.close()
            raise


if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.start()
    print ('Goodbye')