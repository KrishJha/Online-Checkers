import socket



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        handle = open('settings.txt', 'r')
        addr = handle.read()
        handle.close()
        self.server = addr
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return (self.client.recv(2048).decode())
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(str(data)))
            return (self.client.recv(2048)).decode()
        except socket.error as e:
            print(e)