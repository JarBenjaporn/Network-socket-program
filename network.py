import socket
import pickle

class RPSCP:
    @staticmethod
    def encode(command, value=None):
        if value:
            return f"{command}:{value}".encode()
        return command.encode()

    @staticmethod
    def decode(message):
        message = message.decode()
        if ':' in message:
            return message.split(':')
        return message, None
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.135"
        self.port = 8080
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(RPSCP.encode(*data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)




