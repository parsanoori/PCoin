import socket
import json


class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"{self.ip}:{self.port}"

    def send(self, message: json):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.sendall(message.encode('utf-8'))
        s.close()
