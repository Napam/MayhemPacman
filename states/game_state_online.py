'''
Module containing the online game class called mayhem

Written by Naphat Amundsen
'''
import pygame as pg
import numpy as np 
import pickle
import time
import itertools
from multiprocessing import Pipe, Process
from importlib import reload

import user_settings as cng
from states import state_config as state_cng
from instances import instance_config as game_cng

from states import state
from states import game_state

from classes import spaceship
from classes import projectile
from classes import maps

from images import images as imgs
from instances import game_instances as game_i
from instances import ui_instances as ui_i

from server import network as net 

FRAME_TIME = 1/cng.fps
COLORS = pg.colordict.THECOLORS

def handshake(bridge, ship):
    '''
    Initialize handshake with server
    This function returns the client_id (int)
    '''
    out_data = pickle.dumps(ship)
    bridge.send(out_data)
    
    client_id = pickle.loads(bridge.recv(state_cng.recv_size))
    
    return client_id

def server_comm_protocol(bridge, pipe, ship, bullets):
    '''
    Stands for server communication protocoll. This function handles the 
    client-server communication, and is meant to be run by a parallell process to
    reduce in-game stuttering.
    '''
    # TODO: Contemplate buffersize, should at least be 16kb
    recv_size = 1024*32
    bridge.client_socket.settimeout(5.0)
    while True:
        try:
            kill_signal, ship, bullets = pipe.recv()
            if(kill_signal):
                pipe.close()
                return
            data_to_send = pickle.dumps([ship, bullets])
            bridge.send(data_to_send)
            
            try:
                all_ships, all_bullets, planets, asteroids = pickle.loads(bridge.recv(state_cng.recv_size))
            except:
                pass

            all_bullets = list(itertools.chain.from_iterable(all_bullets))
            
            pipe.send([all_ships, all_bullets, planets, asteroids])
        except:
            print("Client comm process terminated")
            pipe.send([0,0,0,0])
            pipe.close()
            return

class mayhem(game_state.mayhem):
    '''
    Multiplayer (LAN) mayhem class, inherits the single-player mayhem class
    and is meant to be a part of a state machine.
    '''
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)

    def init_attributes(self):
        '''Helper method for initializing attributes, used for soft-reloading'''
        self.planets = []
        self.asteroids = []
        self.all_ships = []
        self.bullets = []
        
        self.ship = game_i.ship
        self.camera = np.array([self.w_shape[0], self.w_shape[1]])/2 - self.ship.pos
        self.show_refuel = False
        self.show_loading_ammo = False
            
    def update_graphics(self):
        '''
        Blits and flips

        The objects does not contain any surface objects to be blitted and therefore
        needs to be given which image to blit. This is because the the objects should 
        be lightweight (and you can't pickle surfaces anyways) in order to be sent
        to a server during an online session.
        '''
        self.WINDOW.fill(self.bg_color)

        self.WINDOW.blit(
            imgs.bg_img,
            self.camera
        )

        self.planets[0].draw(self.WINDOW, self.camera, imgs.earth_img)
        self.planets[1].draw(self.WINDOW, self.camera, imgs.venus_img)
        game_i.sun.draw(self.WINDOW, self.camera, imgs.sun_img)

        for ship in self.all_ships:
            ship.draw(self.WINDOW, self.camera, imgs.enemyship_img)

        for asteroid, img in zip(self.asteroids, imgs.asteroid_imgs):
            asteroid.draw(self.WINDOW, self.camera, img)
        
        for bullet in self.all_bullets:
            bullet.draw(self.WINDOW, self.camera, imgs.bullet_img)

        self.ship.draw(
            self.WINDOW,
            self.camera,
            imgs.ship_img
        )

        self.minimap.draw(
            WINDOW=self.WINDOW,
            colors=game_i.minimap_colors_online,
            sizes=game_i.minimap_sizes_online,
            bullets=self.all_bullets,
            sun=[game_i.sun],
            celestials=self.planets,
            asteroids=self.asteroids,
            others=self.all_ships,
        )

        self.minimap.draw_player(
            self.WINDOW,
            game_i.ship, 
            2
        )

        for text in ui_i.indicators:
            text.draw(self.WINDOW)
        pg.display.update()
    
    def logic(self):
        '''
        Method for handling logic 
        '''
        self.ship.update(self)
        
        for bullet in self.bullets:
            bullet.update(self)
            bullet.interact_ship(self.all_ships, self.bullets)

    def parallell_comm_protocol(self, pipe):
        '''
        Stands for parallell communication protocoll, and is the 
        function that is meant to be called from the main process to communicate
        with the parallell process via a pipe.
        '''
        self.all_ships, self.all_bullets, self.planets, self.asteroids = pipe.recv()
        if self.all_ships == 0:
            return 0
        del(self.all_ships[self.client_id])
        self.all_ships = list(self.all_ships.values())
        return 1

    def run(self):
        '''
        The "main" loop 
        '''
        self.socket = net.Network()

        # If socket fails to connect to server
        if not self.socket.connect():
            self._active = False
            return self.MANAGER.get_state('main_menu')
        
        state_pipe, comm_pipe = Pipe()

        self.client_id = handshake(self.socket, self.ship)
        print(f"Client id = {self.client_id}")

        # Run server communication protocol in separate process
        p = Process(target=server_comm_protocol, args=(self.socket, comm_pipe, self.ship, self.bullets))
        p.start()

        while(self._active):
            state_pipe.send((0, self.ship, self.bullets)) 
            if not self.parallell_comm_protocol(state_pipe):
                self._active = False
                self.next_state = self.MANAGER.get_state('main_menu')
                break
            self.dt = self.clock.tick(cng.fps)

            # TODO: Check if this works properly for high fps
            self.lag_correction = self.dt/self.target_timestep              
            
            self.update_graphics()
            self.update_user_input()
            self.logic()

            # This needs to be below update graphics for some reason
            self.animations()
        
        # Terminate parallell process by telling it to kill itself
        state_pipe.send((1, None, None))
        self.socket.client_socket.close()
        
        p.join()
        # p.close happens automatically during garbage collection, and using p.close raises attribute error for some computers
        # p.close()
            
        return self.next_state

        
