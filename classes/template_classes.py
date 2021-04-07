'''
Module containing template classes

Written by Naphat Amundsen
'''
import abc
import pygame
import numpy as np

class game_object(abc.ABC):
    def __init__(self, pos, init_dir, init_vel):
        self.pos = np.array(pos) 
        self.vel = np.array(init_vel)
        self.dir = np.array(init_dir)

    @abc.abstractmethod    
    def draw(self, WINDOW):
        '''Method for drawing must be explicitly implemented in child class'''
    
    def draw_dot(self, WINDOW, color=[255,255,255], radius=5, camera=None):
        '''
        Draws a dot the position of the object. Generally used for 
        debugging purposes.
        '''
        if(camera):
            pygame.draw.circle(
                WINDOW,
                color,
                (self.pos+camera).astype('int'),
                radius
            )
        else:
            pygame.draw.circle(
                WINDOW,
                color,
                self.pos.astype('int'),
                radius
            )
    
    def draw_radius(self, WINDOW, color=[255,255,255], radius=10, thickness=1, camera=None):
        '''
        Draws a hollow circle around position of the object. Generally used for 
        debugging purposes.
        '''
        if(camera):
            pygame.draw.circle(
                WINDOW,
                color,
                (self.pos+camera).astype('int'),
                radius,
                thickness
            )
        else:
            pygame.draw.circle(
                WINDOW,
                color,
                self.pos.astype('int'),
                radius,
                thickness
            )
    
    @staticmethod
    def rotmatrix(d_omega):
        sin = np.sin(d_omega)
        cos = np.cos(d_omega)

        return [[cos, -sin],[sin, cos]]




        
