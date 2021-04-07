'''
This .py file is just a general template that works well with
the rest of the framework. If you would want to integrate another 
kind of state to the framework, the only requirements are:

The state class (in this template it's "name") needs to have an 
"activate" and "run" method. A reload method is optional.

Written by Naphat Amundsen
'''

import pygame as pg
from states import state
import user_settings as cng

# Change this
from instances import menu_instances as menu_i


class name(state.state):
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        self.fps = cng.fps

    def update_graphics(self):
        '''
        Blits and flips
        '''

        # Change to this
        for instance in menu_i.instance_list:
            instance.draw(self.WINDOW)

        pg.display.update()


    def animations(self):
        '''
        Method that handles animations, which are
        changes in graphics that does not affect the game
        '''
        pass


    def interact_user(self):
        '''
        Method for user interactions
        '''
        pass
    

    def logic(self):
        '''
        Method for handling logic 
        '''
        pass 
        

    def run(self):
        '''
        The "main" loop 
        '''
        while self._active:
            self.clock.tick(cng.fps)
            self.update_user_input()
            self.interact_user()
            self.logic()
            self.update_graphics()

            # This needs to be below update graphics for some reason
            self.animations()

        return self.next_state
    

    def reload(self):
        '''
        Method for doing soft reload
        '''
        pass