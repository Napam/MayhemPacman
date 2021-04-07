'''
Module containing the main menu class called menu

Writen by Naphat Amundsen
'''
import numpy as np
import pygame as pg
from states import state
import user_settings as cng

from instances import main_menu_instances as menu_i
from images import images
import time

class menu(state.state):
    '''Main menu class, inherits state.state and is meant to be a part of a state machine'''
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        self.fps = cng.fps
        self.bg_pos = np.zeros(2)

    def update_graphics(self):
        '''
        Blits and flips
        '''
        self.WINDOW.blit(
            images.menu_img,
            self.bg_pos
        )

        for button in menu_i.all_to_be_drawn:
            button.draw(self.WINDOW)
        
        pg.display.update()

    def interact_user(self):
        '''
        Method for user interactions
        '''
        for button in menu_i.state_buttons:
            button.interact_mouse(self.mouse_pos, self.click)

    def logic(self):
        '''
        Method for handling logic 
        '''
        for button in menu_i.state_buttons:
            if button.state:
                button.state = False
                self.change_state_to(next_state=button.next_state, reload=True)

    def run(self):
        '''
        The "main" loop 
        '''
        while(self._active):
            self.clock.tick(cng.fps)
            self.update_user_input()
            self.interact_user()
            self.logic()
            self.update_graphics()
        return self.next_state
    
    def reload(self):
        '''
        Method for doing soft reload, needed for compitability with state machine
        '''
        pass