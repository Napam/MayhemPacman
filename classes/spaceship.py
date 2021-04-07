'''
Module containing the spaceship class

Written by Naphat Amundsen
'''

import pygame as pg 
import numpy as np
from classes import template_classes
from classes import projectile

from classes import class_config as cng

class spaceship(template_classes.game_object):
    '''
    Class for the in-game player controllled spaceship object. 
    '''
    def __init__(self, pos, init_dir):
        super().__init__(pos, init_dir, (0,0))
        self.fire_lag = 0
        self.jump_lag = 0
        self.reload_lag = 0
        
        self.fuel = cng.max_fuel
        self.ammo = cng.max_ammo
        self.hp = cng.max_hp

    def __str__(self):
        return f"Ship at: {self.pos}, dir: {self.dir}"
        
    def draw(self, WINDOW, camera, img):
        '''
        Draws the spaceship with the camera offset (to center the spaceship)
        '''
        rot_img = pg.transform.rotate(img, np.degrees(np.arctan2(*self.dir))-90)
        rot_img_rect = rot_img.get_rect(center=self.pos)

        WINDOW.blit(
            rot_img,
            (rot_img_rect.x + camera[0], rot_img_rect.y + camera[1])
        )

    def thrust(self, reverse=False):
        '''Method for engine thrust'''
        if(self.fuel > 0):
            if(reverse):
                self.vel -= cng.reverse_multiplier*cng.a_thrust*self.dir
            else:
                self.vel += cng.a_thrust*self.dir
            
            if(self.fuel):
                self.fuel -= 1
    
    def rotate(self, angle, lag_correction):
        '''Rotates the ships direction given an angel and a lag correction scalar'''
        if(self.fuel > 0):
            self.dir = self.rotmatrix(lag_correction*angle)@self.dir
            self.fuel -= 1

    def interact_user(self, state):
        '''
        Handles regular spaceship movement using WASD keys
        '''
        if(state.kbinput[pg.K_w]):
            self.thrust(reverse=False)
        if(state.kbinput[pg.K_a]):
            self.rotate(-cng.omega, lag_correction=state.lag_correction)
        if(state.kbinput[pg.K_s]):
            self.thrust(reverse=True)
        if(state.kbinput[pg.K_d]):
            self.rotate(cng.omega, lag_correction=state.lag_correction)

    def refuel(self, state):
        '''
        Method for refueling proceedure
        '''
        if self.fuel < cng.max_fuel:
            self.fuel += int(state.lag_correction*cng.refuel_rate)
            state.show_refuel = True
        else:
            self.fuel = cng.max_fuel
            state.show_refuel = False

    def load_ammo(self, lag_correction):
        '''
        Method for reloading proceedure
        '''
        if(self.reload_lag < 1):
            self.ammo += cng.reload_rate
            self.reload_lag = cng.reload_lag
        else:
            self.reload_lag -= int(lag_correction*1)

    def planet_gravity(self, planet_obj, long_const=80000, close_const=0.3):
        '''
        Method that makes the spaceship feel a given planet's gravitational
        force given a reference to a planet object (or any object with a pos attribute). 

        Returns whether or not the ship is in planets inner 
        radius
        '''
        dir_to_planet = planet_obj.pos - self.pos
        dist_to_planet = np.linalg.norm(dir_to_planet)
        dir_to_planet = dir_to_planet/dist_to_planet

        if dist_to_planet > cng.inner_planet_gravity_radius:
            self.vel = self.vel + (long_const/dist_to_planet**2)*dir_to_planet             
            return 0
        else: 
            self.vel = 0.99*self.vel + close_const*dir_to_planet
            return 1

    def game_over(self, state):
        '''Method for game over proceedure'''
        state.next_state = state.MANAGER.get_state('game_over')
        state._active = False

    def in_border(self, state):
        '''Method to contain ship within the game map'''
        if(self.pos[0] <= 0):
            self.vel[0] = 0
            self.vel += cng.a_thrust*cng.RIGHT
        
        if(self.pos[0] >= state.map.shape[0]):
            self.vel[0] = 0
            self.vel += cng.a_thrust*cng.LEFT

        if(self.pos[1] <= 0):
            self.vel[1] = 0
            self.vel += cng.a_thrust*cng.DOWN

        if(self.pos[1] >= state.map.shape[1]):
            self.vel[1] = 0
            self.vel += cng.a_thrust*cng.UP

    def interact_sun(self, state):
        '''
        Method to make the ship feel the gravitational force to the center of the map.
        As well as invoking the game_over method if the ship is within some distance 
        from the center. 
        '''
        dir_to_center = state.map.center-self.pos
        dist_to_center = np.linalg.norm(dir_to_center)
        dir_to_center = dir_to_center/dist_to_center
        self.vel = self.vel + (cng.radial_force_constant/dist_to_center**2)*dir_to_center

        if dist_to_center < cng.sun_center_delete_radius:
            self.game_over(state)

    def interact_venus(self, state):
        '''
        Specialized method to make the spaceship feel the gravitational pull
        to Venus. This method also invokes the refuel proceedure if the ship is 
        within som distance from Venus.
        '''
        if self.planet_gravity(state.planets[1], 70000, 0.5):    
            self.refuel(state)

    def interact_earth(self, state):
        '''
        Specialized method to make the spaceship feel the gravitational pull to Earth.
        This method invokes the ammo reloading proceedure if the ship is within som 
        distance from Earth.  
        '''
        if self.planet_gravity(state.planets[0], 90000, 0.3):
            if self.ammo < cng.max_ammo:
                state.show_loading_ammo = True
                self.load_ammo(state.lag_correction)
            else:
                state.show_loading_ammo = False

    def interact_asteroid(self, asteroids):
        '''
        Method for handling collisions with asteroids
        '''
        for asteroid in asteroids:
            if np.linalg.norm(asteroid.pos-self.pos) < cng.asteroid_collision_radius:
                self.hp -= np.linalg.norm(asteroid.vel)//6
                self.vel = 0.85*self.vel + 0.15*asteroid.vel

    def interact_bullets(self, bullets):
        '''
        Method for handling collisions with bullets
        '''
        for bullet in bullets:
            if np.linalg.norm(bullet.pos-self.pos) < cng.bullet_collision_radius:
                self.hp -= 10
                self.vel = 0.85*self.vel + 0.15*bullet.vel

    def drag_force(self):
        '''
        Method to make the spaceship feel a dragforce ("air resistance")
        '''
        self.vel = self.vel - cng.f_drag*self.vel

    def fire(self, state):
        '''
        Method for firing bullets. Appends bullets to a designated bullet list 
        in the state.
        '''
        if self.ammo:
            if self.fire_lag < 1:
                if state.kbinput[pg.K_SPACE]:
                    state.bullets.append(
                        projectile.bullet(self.pos, self.dir, state.lag_correction*self.vel)
                    )
                    self.ammo -= 1
                    self.fire_lag = cng.fire_lag
            else: 
                self.fire_lag -= int(state.lag_correction*1)

    def hyperjump(self, state):
        '''
        Method for doing a hyperjump
        
        The key is 'J' for hyperjump
        '''
        if self.fuel > cng.hyperjump_cost:
            if self.jump_lag < 1:
                if state.kbinput[pg.K_j]:
                    self.vel += cng.hyperjump_multiplier*cng.a_thrust*self.dir
                    self.jump_lag = cng.jump_lag
                    self.fuel -= cng.hyperjump_cost
            else:
                self.jump_lag -= 1

    def motion(self, state):
        '''
        Method for integration the velocity into the position of the ship.

        Also handles the camera adjustment 

        This method should be called after calculating all the forces
        '''
        self.pos = self.pos + state.lag_correction*self.vel
        state.camera = state.camera - state.lag_correction*self.vel  

    def check_dead(self, state):
        '''Checks whether the ships HP is empty, invoke game over method if True'''
        if self.hp <= 0:
            self.game_over(state)

    def update(self, state):
        ''' 
        Update method for the spaceship. Simply calls all the 
        method that are included in one iteration
        '''
        self.check_dead(state)
        self.in_border(state)

        self.interact_user(state)
        self.interact_venus(state)
        self.interact_earth(state)
        self.interact_sun(state)
        self.interact_asteroid(state.asteroids)
        self.interact_bullets(state.all_bullets)
        
        self.drag_force()
        self.fire(state)
        self.hyperjump(state)
        self.motion(state)
