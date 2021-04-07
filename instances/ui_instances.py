'''
Module containing varius user interface instances
such as text and button objects related to the Mayhem game.

Written by Naphat Amundsen
'''
import sys 

sys.path.insert(0, '..')

import pygame as pg 
from classes import interface as ui
import user_settings as user_cng 
# from instances import instance_config as game_cng 
from instances import instance_config as cng

COLORS = pg.colordict.THECOLORS
pg.font.init()


# The objects that have somewhat nonsensible texts 
# will have their rendered text changed during runtime as they are actively rendered
indicators = [
    ui.text_float_active(
        text='Fuel indicator',        
        pos=(user_cng.w_shape[0]*0.03, user_cng.w_shape[1]*0.04),        
        color=COLORS['white'],        
        font=cng.font,        
        font_size=cng.game_indicator_fsize,        
    ),
    ui.text_float_active(
        text='HP indicator',        
        pos=(user_cng.w_shape[0]*0.03, user_cng.w_shape[1]*0.07),        
        color=COLORS['white'],        
        font=cng.font,        
        font_size=cng.game_indicator_fsize,        
    ),
    ui.text_float_active(
        text='Ammo  indicator',        
        pos=(user_cng.w_shape[0]*0.03, user_cng.w_shape[1]*0.1),        
        color=COLORS['white'],        
        font=cng.font,        
        font_size=cng.game_indicator_fsize,        
    ),
    ui.text_float_active(
        text='FPS  indicator',        
        pos=(user_cng.w_shape[0]*0.03, user_cng.w_shape[1]*0.95),        
        color=COLORS['gray'],        
        font=cng.font,        
        font_size=cng.game_indicator_fsize,        
    )
]

refueling = ui.centered_indicator(
    text='Refueling...',        
    pos=[None, user_cng.w_shape[1]*0.75],        
    color=COLORS['white'],        
    font=cng.font,        
    font_size=cng.game_indicator_fsize,  
    window_shape=user_cng.w_shape,        
)

loading_ammo = ui.centered_indicator(
    text='Loading ammo...',        
    pos=[None, user_cng.w_shape[1]*0.75],        
    color=COLORS['white'],        
    font=cng.font,        
    font_size=cng.game_indicator_fsize,  
    window_shape=user_cng.w_shape,        
)

indicators.append(refueling)
indicators.append(loading_ammo)

game_over = ui.text_center_active(
    text='GAME OVER',        
    pos=[None, user_cng.w_shape[1]*0.2],        
    color=COLORS['white'],        
    font=cng.font,        
    font_size=cng.game_over_fsize,  
    window_shape=user_cng.w_shape,
)

game_over_msg = ui.text_center_active(
    text='Returning to main menu...',        
    pos=[None, user_cng.w_shape[1]*0.5],        
    color=COLORS['white'],        
    font=cng.font,        
    font_size=cng.game_over_fsize,  
    window_shape=user_cng.w_shape,
)
