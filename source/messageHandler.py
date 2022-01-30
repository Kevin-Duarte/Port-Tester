import socket
import threading
import os
import time


class messageHandler:
    def __init__(self) -> None:
        pass

    def sendTCP(self, host, message, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(message.encode())

    def receiveTCP(self, host, port, timeout):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                return data, addr

    def sendUDP(self, host, message, port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(message.encode(), (host, port))

    def receiveUDP(self, host, port, timeout):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.bind((host, port)) 
            message, addr = s.recvfrom(1024)
            return message, addr
           