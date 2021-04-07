'''
Module containing classes for celestial bodies (planets)

Written by Naphat Amundsen
'''
import pygame as pg 
import numpy as np

from classes import template_classes

class planet(template_classes.game_object):
    '''
    Class for a planet object. The planet object feels a force pulling the object 
    towards the state's map's center. 

    Inherits the template object 'game_object'. 
    '''
    def __init__(self, pos, init_vel, init_dir, rforce):
        super().__init__(pos, init_dir, init_vel) 
        self.f_radial_const = rforce
    
    def draw(self, WINDOW, camera, img):
        '''Blits given image at position offset by camera'''
        self.pos = self.pos.astype('int')
        centered_pos = img.get_rect(center=self.pos)

        WINDOW.blit(
            img,
            [centered_pos.x, centered_pos.y]+camera
        )

    def draw_rotate(self, WINDOW, camera, img, degrees):
        '''
        Blits given image at position offset by camera, takes in additional 
        argumet degrees for blitting a rotated version of the image
        '''
        rot_img = pg.transform.rotate(img, degrees)
        rot_img_rect = rot_img.get_rect(center=self.pos)

        WINDOW.blit(
            rot_img,
            (rot_img_rect.x + camera[0], rot_img_rect.y + camera[1])
        )

    def radial_force(self, state):
        '''
        Method to make planets feel the gravitational pull towards the given state's map object's center
        '''
        dir_to_middle = state.map.center-self.pos
        dist_to_middle = np.linalg.norm(dir_to_middle)
        dir_to_middle = dir_to_middle/dist_to_middle

        self.vel = self.vel + (self.f_radial_const/dist_to_middle**2)*dir_to_middle

    def motion(self):
        '''
        Method for integration velocity into position. Motion is not 
        lag corrected (haven't bothered calculating the required adjustment
        in the numerator of GMm/r^2 to conserve the trajectory with a lag 
        correction scalar)
        '''
        self.pos = self.pos + self.vel
    
    def update(self, state):
        '''Updates planet behavior'''
        self.radial_force(state)
        self.motion()
        

class rotating_planet(planet):
    '''
    Inherits planet and simply has an angle and anglespeed. The additional attributes 
    are used for drawing a rotating planet. The attributes gets updated when the
    planet moves. 

    This class if used for asteroids as well. 
    '''
    def __init__(self, pos, init_vel, init_dir, r_force, omega):
        super().__init__(pos, init_vel, init_dir, r_force)
        self.theta = 0
        self.omega = omega
    
    def motion(self):
        '''
        Method for integration velocity into position. Motion is not 
        lag corrected (haven't bothered calculating the required adjustment
        in the numerator of GMm/r^2 to conserve the trajectory with a lag 
        correction scalar)
        '''
        self.pos = self.pos + self.vel
        self.theta = (self.theta+self.omega) % 360

    def draw(self, WINDOW, camera, img):
        '''This exists (even though draw_rotate already is in scope) to ensure compitability in the state'''
        rot_img = pg.transform.rotate(img, self.theta)
        rot_img_rect = rot_img.get_rect(center=self.pos)

        WINDOW.blit(
            rot_img,
            (rot_img_rect.x + camera[0], rot_img_rect.y + camera[1])
        )


