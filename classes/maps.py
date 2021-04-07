'''
Module containing game map class and minimap class

Written by Naphat Amundsen
'''

import numpy as np 
import pygame as pg 

from classes import class_config as cng

class minimap:
    '''Minimap class'''
    def __init__(self, gmap, w_shape, w_norm):
        '''Calculates minimap position and shape on-screen'''
        self.w_shape = w_shape
        self.gmap_shape = gmap.shape

        size = cng.minimap_size

        # Calculates map shape to fit window properly
        # (derived from solving a linear system)
        self.shape = np.zeros(2)
        self.shape[1] = np.sqrt(size**2/(1+gmap.ratio**2))
        self.shape[0] = gmap.ratio*self.shape[1]
        
        self.surface = pg.Surface(self.shape)
        self.surface.set_alpha(cng.minmap_alpha)
        self.surface.fill(cng.minimap_color)
        self.pos = np.empty(2)

        # Calculate minimap position to fit window properly
        # (also derived from solving a linear system)
        L = w_norm*cng.minimap_pos_multiplier
        self.pos[0] = w_shape[0] - L - self.shape[0]
        self.pos[1] = L
        
        size = w_shape/self.gmap_shape*self.shape

        self.view = pg.Rect((0,0,*size))

    def draw_player(self, WINDOW, player, size=2):
        '''Draws player with field of view box'''
        minimap_pos = player.pos/self.gmap_shape
        minimap_pos = minimap_pos*self.shape + self.pos
        self.view.center = minimap_pos

        pg.draw.rect(WINDOW, cng.minimap_fov_color, self.view, 1)

        pg.draw.circle(
            WINDOW,
            cng.minimap_player_color,
            minimap_pos.astype(int),
            size
        )

    def draw(self, WINDOW, colors, sizes, **objects):    
        '''Draws minimap'''
        WINDOW.blit(self.surface, self.pos)

        keys = list(objects.keys())
        for val, key in enumerate(keys):
            objs = objects[key]
            for obj in objs:
                minimap_pos = obj.pos/self.gmap_shape
                minimap_pos = minimap_pos*self.shape + self.pos
                
                pg.draw.circle(
                    WINDOW,
                    colors[val],
                    minimap_pos.astype(int),
                    sizes[val]
                )

class game_map:
    '''
    Game map object

    Only has an init function which calculates
    map attributes: shape, ratio, norm, center

    Just to keep things nice and tidy
    '''
    def __init__(self, map_shape):
        self.shape = np.array(map_shape)
        self.ratio = self.shape[0]/self.shape[1]
        self.norm = np.linalg.norm(self.shape)
        self.center = self.shape/2 

        
