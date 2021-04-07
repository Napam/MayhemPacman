'''
Module containing game_over state

Written by Naphat Amundsen
'''
import sys 
sys.path.insert(0, '..')

import time
import pygame as pg

from states import state
import user_settings as cng

from instances import ui_instances as ui_i
from images import images

class game_over(state.state):
    '''Game over class, a transitional state in the state machine. Used for game-over screen'''
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        self.fps = cng.fps/2

        self.surface = pg.Surface(cng.w_shape)
        self.surface.set_alpha(30)
        self.surface.fill([80,80,80])
    
    def update_graphics(self):
        '''
        Blits and flips
        '''
        if time.time() - self.t0_gray > 0.05:
            self.t0 = time.time()
            self.WINDOW.blit(
                self.surface,
                (0,0)
            )

        ui_i.game_over.draw(self.WINDOW)
        ui_i.game_over_msg.draw(self.WINDOW)
        
        pg.display.update()

    def logic(self):
        '''
        Method for handling logic 
        '''
        if time.time() - self.t0_exit > 2:
            self.change_state_to('main_menu')

    def run(self):
        '''
        The "main" loop 
        '''
        self.t0_gray = time.time()
        self.t0_exit = time.time()

        while(self._active):
            self.clock.tick(cng.fps)
            self.update_user_input()
            self.logic()
            self.update_graphics()
        return self.next_state

    def reload(self):
        '''
        Method for doing soft reload
        '''
        pass
    