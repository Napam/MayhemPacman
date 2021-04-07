'''
Info-screen state

Written by Naphat Amundsen
'''

import pygame as pg 
from states import state
import user_settings as cng

# Change this
from instances import info_instances_spacemayhem as info_i
from images import images

class info(state.state):
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        self.fps = cng.fps/2

        self.dark_surface = pg.Surface(cng.w_shape, flags=pg.SRCALPHA)
        self.dark_surface.fill((100, 100, 100, 0))

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
        
    def run(self):
        '''
        The "main" loop 
        '''
        while self._active:
            self.clock.tick(cng.fps)
            self.update_user_input()
            self.interact_user()
            self.update_graphics()
        return self.next_state

    def reload(self):
        '''
        Method for doing soft reload
        '''
        pass