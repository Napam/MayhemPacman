'''
Module containing adapter classes for server.py 

The server code needs to be as "barebones" as possible
to avoid various of errors. Adapters are required
to make that possible.

Written by Naphat Amundsen
'''

class server_game_state:
    '''
    Used as an adapter to bring necessary information to server.py.
    The server requires this to calculate the movement of celestial bodies in 
    a multiplayer game.
    '''
    def __init__(self, game_map):
        self.map = game_map