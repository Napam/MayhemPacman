'''
Module containing the bullet class

Written by Naphat Amundsen
'''

import pygame as pg 
import numpy as np 
from classes import template_classes
import time

from classes import class_config as cng

class bullet(template_classes.game_object):
    '''Class for ingame bullets'''
    def __init__(self, pos, init_dir, ship_vel):
        super().__init__(pos, init_dir, ship_vel)
        self.start_t = time.time()
        self.pos = self.pos+cng.initial_pos_offset*self.dir
        self.vel = cng.initial_bullet_velocity*self.dir+ship_vel

    def draw(self, WINDOW, camera, img):
        '''
        Blits given image to the window at a positio offset by camera
        '''
        
        self.pos = self.pos.astype('int')
        centered_pos = img.get_rect(center=self.pos)

        WINDOW.blit(
            img,
            [centered_pos.x, centered_pos.y]+camera
        )
    
    def motion(self, state):
        '''Integrates velocity into bullet's position '''
        self.pos = self.pos + state.lag_correction*self.vel

    def interact_sun(self, state):
        '''
        Method to make bullet feel gravitational pull center of state's map object.
        Will delete self if self.pos is within some distance from the center
        '''
        dir_to_middle = state.map.center-self.pos
        dist_to_middle = np.linalg.norm(dir_to_middle)
        dir_to_middle = dir_to_middle/dist_to_middle
        self.vel = self.vel + (cng.bullet_radial_force_constant/dist_to_middle**2)*dir_to_middle

        if dist_to_middle < cng.sun_center_delete_radius:
            state.bullets.remove(self)
    
    def interact_ship(self, ships, bullet_list):
        '''To delete bullet from game if collision with a ship'''
        for ship in ships:
            if np.linalg.norm(ship.pos-self.pos) < cng.bullet_collision_radius2:
                bullet_list.remove(self)

    def update(self, state):
        '''
        Update bullet behavior
        
        Deletes self after some time.
        '''
        self.interact_sun(state)
        self.motion(state)
        if((time.time()-self.start_t) > 2):
            state.bullets.remove(self)
        