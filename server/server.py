'''
Running this file (as the main file) will run the LAN server
with the configuration found in user_settings.py. 

This program is meant to be run from the server menu

Written by Naphat Amundsen
'''

import sys
sys.path.insert(0,'..')
# Make adjacent modules visible

import socket
import _thread 
import numpy as np
import pickle
import traceback
import user_settings as cng
import time

from instances import server_instances as server_i
from instances import game_instances as game_i
from states import state_config as state_cng


def handshake(client_socket, ship_objects, client_id):
    '''
    Initialize handshake with client. Updates necessary objects 
    in-place using the given references.
    '''
    try:
        client_ship = pickle.loads(client_socket.recv(state_cng.recv_size))
        ship_objects.update({client_id:client_ship})
        projectile_objects.update({client_id:[]})
        client_socket.send(pickle.dumps(client_id))
    except Exception:
        print("Handshake failed")
        traceback.print_exc()
        return

def client_comm_protocol(client_socket, ship_objects, projectile_objects, client_id):
    '''Stands for client communication protocol, and is the communication process between the server and a client'''
    recv_size = 1024*16
    while True:
        try:
            # TODO: Think over this try try thing
            try:
                client_ship, client_bullets = pickle.loads(client_socket.recv(recv_size))
            except:
                raise socket.error

            ship_objects[client_id] = client_ship
            projectile_objects[client_id] = client_bullets

            all_bullets = list(projectile_objects.values())

            data_to_send = pickle.dumps([
                ship_objects, 
                all_bullets, 
                game_i.planets, 
                game_i.asteroids
            ])

            client_socket.send(data_to_send)

        except socket.error:
            break
    
    print(f"Lost connection with client {client_id}")
    print(f"Removing objects bound to client {client_id}\n")
    ship_objects.pop(client_id)
    projectile_objects.pop(client_id)
    return

def server_objects():
    '''Update motion of celestial bodies'''
    while True:
        for celestial in game_i.all_celestials:
            celestial.update(server_i.celestial_state_adapter)

        time.sleep(1/cng.fps)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if cng.server == 'host':
        server = socket.gethostbyname(socket.gethostname())
    else:
        server = cng.server
    port = cng.port
    address = (server, port) 
    
    try: 
        server_socket.bind(address)
    except:
        print("Server socket failed to bind, are there any other server instances running?")
        exit()

    server_socket.listen(4)
    print(f"LAN server initialized at {address}")

    ship_objects = {}
    projectile_objects = {}

    # Calculates motion of celestial bodies in a pseudo-thread
    _thread.start_new_thread(server_objects, ())

    client_id = 0
    while True:
        client_socket, client_address = server_socket.accept() 
        print("Connection established with ", client_address)

        handshake(client_socket, ship_objects, client_id) 
        _thread.start_new_thread(client_comm_protocol, (client_socket, ship_objects, projectile_objects, client_id))   
        client_id += 1
       
            


