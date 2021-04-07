'''
The main python file. Execute this file to 
run program.

Written by Naphat Amundsen 👌🤣🤣🤣
'''
import pygame as pg 
import numpy as np 
from importlib import reload
from json import loads

from instances import game_instances as game_i

from states import manager
from states import game_state
from states import game_state_online
from states import main_menu
from states import server_menu
from states import game_over_state
from states import mayham
from states import info_state_spacemayhem
from states import info_state_pacmanmayhem

from images import images

import user_settings as cng

class main_class:
    '''The "controller" class that contains all information related to the running program'''
    def __init__(self):
        pg.init()
        if(cng.fullscreen):
            WINDOW = pg.display.set_mode(cng.w_shape, pg.FULLSCREEN)
        else:
            WINDOW = pg.display.set_mode(cng.w_shape)

        pg.display.set_caption("MAYHEM")
        
        # The manager class is essentially a container for class instances (with additional
        # functionality, see the class definition in objects/manager.py). The manager 
        # abstracts away most of the code for switching between class instances during 
        # runtime. 
        #
        # In this case, the manager is utilized as a server for "states". States are the
        # class instances, where the classes can be interpreted as standalone programs.  
        
        manager0 = manager.manager(state_kwargs={'WINDOW':WINDOW})

        # Necessary to initalize images from images module
        images.init(WINDOW)

        # Add states to manager
        manager0.update(
            new_states = {
                'main_menu':main_menu.menu(manager0, WINDOW),
                'server_menu':server_menu.server_menu(manager0, WINDOW),
                'mayhem':game_state.mayhem(manager0, WINDOW),
                'mayhem_online':game_state_online.mayhem(manager0, WINDOW),
                'game_over':game_over_state.game_over(manager0, WINDOW),
                'pacman_game':mayham.Game(manager0,WINDOW),
                'info_spacemayhem':info_state_spacemayhem.info(manager0,WINDOW),
                'info_pacmanmayhem':info_state_pacmanmayhem.info(manager0,WINDOW),
            }
        )
    
        # Initial state
        current_state = manager0.get_state('main_menu')
        
        # Turn local variables to instance attributes
        self.__dict__.update(locals())

    def run(self):
        '''Method that initializes the state machine system'''
        while(True):
            self.current_state.activate()
            # The current state should return the next state when its deactivated
            self.current_state = self.current_state.run()

            # If exit state is returned (a None type)
            if(not self.current_state):
                # Necessary to properly close down the server menu in case of 
                # a running server 
                server_menu_instance = self.manager0.get_state('server_menu')
                server_menu_instance.exit_protocoll()
                break


if __name__ == '__main__':
    MAYHEM = main_class()
    MAYHEM.run()




