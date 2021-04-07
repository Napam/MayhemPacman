'''
Info-screen state

Written by Naphat Amundsen
'''

import pygame as pg 
from states import state
import user_settings as cng

# Change this
from instances import info_instances_pacmanmayhem as info_i
from states import info_state_spacemayhem
from images import images

class info(info_state_spacemayhem.info):
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        
    def update_graphics(self):
        '''
        Blits and flips
        '''
        self.WINDOW.blit(
            images.menu_img,
            (0,0)
        )

        self.WINDOW.blit(
            self.dark_surface,
            (0,0),
            special_flags=pg.BLEND_RGBA_SUB
        )
        

        # Change to this
        for text in info_i.draw_list:
            text.draw(self.WINDOW)

        pg.display.update()

    def interact_user(self):
        '''
        Method for user interactions
        '''     
        info_i.back_button.interact_mouse(self.mouse_pos, self.click)
        if info_i.back_button.state:
            self.change_state_to(info_i.back_button.next_state)