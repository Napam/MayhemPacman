'''
Module containing the main menu instances

Written by Naphat Amundsen
'''

import sys 
sys.path.insert(0, '..')

from classes import interface
from instances import instance_config as icng
import pygame as pg 

COLORS = pg.colordict.THECOLORS

text = [
    interface.text_center(
        text='MAYHEM 2: ELECTRIC BOOGALOO',
        pos=[None, icng.w_shape[1]*0.05],
        color=COLORS['maroon'],
        font=icng.font,
        font_size=icng.mayhem_title_fsize,
        window_shape=icng.w_shape
    )
]

state_buttons = [
    interface.button_center_change_state(
        text='Explore in singleplayer', 
        pos=[None, icng.w_shape[1]*0.15], 
        color=COLORS['beige'], 
        color_mouseover=COLORS['cyan'], 
        font=icng.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=icng.w_shape, 
        next_state='mayhem'
    ),
    interface.button_center_change_state(
        text='Online multiplayer', 
        pos=[None, icng.w_shape[1]*0.25], 
        color=COLORS['beige'], 
        color_mouseover=COLORS['cyan'], 
        font=icng.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=icng.w_shape, 
        next_state='mayhem_online'
    ),
    interface.button_center_change_state(
        text='Server menu', 
        pos=[None, icng.w_shape[1]*0.35], 
        color=COLORS['beige'], 
        color_mouseover=COLORS['cyan'], 
        font=icng.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=icng.w_shape, 
        next_state='server_menu'
    ),
    interface.button_center_change_state(
        text='Pacman cage fight', 
        pos=[None, icng.w_shape[1]*0.45], 
        color=COLORS['beige'], 
        color_mouseover=COLORS['cyan'], 
        font=icng.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=icng.w_shape, 
        next_state='pacman_game'
    ),
    interface.button_center_change_state(
        text='Information about Mayhem 2: Electric Boogaloo', 
        pos=[None, icng.w_shape[1]*0.65], 
        color=COLORS['beige'], 
        color_mouseover=COLORS['cyan'], 
        font=icng.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=icng.w_shape, 
        next_state='info_spacemayhem'
    ),
    interface.button_center_change_state(
        text='Information about Pacman cage fight', 
        pos=[None, icng.w_shape[1]*0.75], 
        color=COLORS['beige'], 
        color_mouseover=COLORS['cyan'], 
        font=icng.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=icng.w_shape, 
        next_state='info_pacmanmayhem'
    ),
    interface.button_center_change_state(
        text='Exit', 
        pos=[None, icng.w_shape[1]*0.90], 
        color=COLORS['beige'], 
        color_mouseover=COLORS['cyan'], 
        font=icng.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=icng.w_shape, 
        next_state='exit'
    ),
]


all_to_be_drawn = text + state_buttons