'''
Module containing the single-player game class called mayhem

Written by Naphat Amundsen
'''
import pygame as pg  
import numpy as np
from importlib import reload

import user_settings as cng
from states import state_config as state_cng

from states import state
from classes import spaceship
from classes import projectile
from classes import planet
from classes import maps

from images import images as imgs
from instances import game_instances as game_i
from instances import ui_instances as ui_i


class mayhem(state.state):
    '''Single-player mayhem class, inherits state.state and is meant to be a part of a state machine'''
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        self.fps = cng.fps
        self.w_shape = cng.w_shape
        self.w_norm = np.linalg.norm(self.w_shape)
        self.bg_color = cng.background_color

        self.target_timestep = np.round(1000/state_cng.game_target_fps)
    
        self.map = game_i.game_map
        self.minimap = game_i.minimap
        self.init_attributes()

    def init_attributes(self):
        '''Helper method for method initializing attributes, used for soft-reloading'''
        self.bullets = []
        self.all_bullets = self.bullets
        self.planets = [game_i.earth, game_i.venus]
        # self.ship = game_i.ship
        self.all_ships = [game_i.ship]
        self.camera = np.array([self.w_shape[0], self.w_shape[1]])/2 - game_i.ship.pos
        self.asteroids = game_i.asteroids
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

        game_i.sun.draw(self.WINDOW, self.camera, imgs.sun_img)
        game_i.earth.draw(self.WINDOW, self.camera, imgs.earth_img)
        game_i.venus.draw(self.WINDOW, self.camera, imgs.venus_img)

        for asteroid, img in zip(game_i.asteroids, imgs.asteroid_imgs):
            asteroid.draw(self.WINDOW, self.camera, img)

        for bullet in self.all_bullets:
            bullet.draw(self.WINDOW, self.camera, imgs.bullet_img)

        game_i.ship.draw(self.WINDOW, self.camera, imgs.ship_img)

        self.minimap.draw(
            WINDOW=self.WINDOW,
            colors=game_i.minimap_colors,
            sizes=game_i.minimap_sizes,
            all_bullets=self.all_bullets,
            sun=[game_i.sun],
            celestials=self.planets,
            asteroids=game_i.asteroids
        )

        self.minimap.draw_player(self.WINDOW, self.all_ships[0], 2)

        for obj in ui_i.indicators:
            obj.draw(self.WINDOW)

        pg.display.update()

    def animations(self):
        '''
        Method that handles animations, which are
        changes in graphics that does not affect the game
        '''
        ui_i.indicators[0].text_r = f"Fuel   {game_i.ship.fuel}"
        ui_i.indicators[1].text_r = f"Health {game_i.ship.hp}"
        ui_i.indicators[2].text_r = f"Ammo   {game_i.ship.ammo}"
        ui_i.indicators[3].text_r = f"FPS    {1000//self.dt}"

        # Passing the ui_i references directly to spaceship.refuel() and figher.load_ammo()
        # did not change the Boolean values in the ui_i instances.
        # This workaround is a quick and dirty fix
        if self.show_refuel:
            ui_i.refueling.show = True
            self.show_refuel = False
        else: 
            ui_i.refueling.show = False
    
        if self.show_loading_ammo:
            ui_i.loading_ammo.show = True
            self.show_loading_ammo = False
        else: 
            ui_i.loading_ammo.show = False

    def logic(self):
        '''
        Method for handling game logic 
        '''
        game_i.ship.update(self)
        game_i.earth.update(self)
        game_i.venus.update(self)

        for asteroid in game_i.asteroids:
            asteroid.update(self)
        
        for bullet in self.all_bullets:
            bullet.update(self)
            # Needs to explicitly call method here for compatibility with the online version
            bullet.interact_ship(self.all_ships, self.all_bullets)

    def run(self):
        '''
        The "main" loop 
        '''
        while(self._active):
            self.dt = self.clock.tick(cng.fps)
            self.lag_correction = self.dt/self.target_timestep
            self.update_user_input()
            self.logic()
            self.update_graphics()

            # This needs to be below update graphics for some reason
            self.animations()
            
        return self.next_state

    def reload(self):
        '''
        Method for doing soft reload
        '''
        reload(game_i)
        self.init_attributes()

