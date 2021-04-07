'''
Network class that acts as a bridge between server and client. An instance
of this should be created in a client. 

Idea taken from:
https://techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/

Written by Naphat Amundsen
'''
import sys 
sys.path.insert(0, '..')
import socket 
import user_settings as cng

class Network:
    '''
    Class that abstracts away the client-side socket code
    '''
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = cng.server if not cng.server == 'host' else socket.gethostbyname(socket.gethostname())
        self.port = cng.port
        self.address = (self.server, self.port)

    def connect(self):     
        '''
        Connects the self.client_socket to give address (from user_settings.py)
        '''
        try:
            self.client_socket.connect(self.address)
            print(f'Client socket connected to {self.address}')
            return 1
        except socket.error as e:
            print('Could not connect to server, assert server address and port in user_settings and assert that the server is running\n')
            print(e)
            return 0

    def send(self, data):    
        '''
        Send data with the socket, socket should be connected using the
        connect() method prior to this
        '''
        try:
            self.client_socket.send(data)
        except socket.error as e:
            print('Could not send data to server socket')
            print(e)

    def recv(self, bufsize=1024):
        '''
        Recieve data 
        '''
        # TODO: Maybe do a try exxcept here?
        return self.client_socket.recv(bufsize)


    
        
