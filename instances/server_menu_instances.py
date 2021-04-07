'''
Module containing server menu instances
such as text and button objects.

Written by Naphat Amundsen
'''
import sys 
sys.path.insert(0, '..')

from classes import interface 
from instances import instance_config as icng

import user_settings as usr 

import pygame as pg

COLORS = pg.colordict.THECOLORS

text = [
    interface.text_center(
        text='SERVER MENU',
        pos=[None, usr.w_shape[1]*0.05],
        color=COLORS['maroon'],
        font=usr.font,
        font_size=icng.mayhem_title_fsize,
        window_shape=usr.w_shape
    )
]

levers = [
    interface.lever_center_active(
        text='Toggle server', 
        pos=[None, icng.w_shape[1]*0.2], 
        color=COLORS['white'], 
        color_mouseover=COLORS['cyan'], 
        color_active=COLORS['gold1'], 
        font=usr.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=usr.w_shape, 
        state=False
    )
]

# Indicator text is actively rendered and will be changed during runtime
indicators = [
    interface.centered_indicator(
        text='Shadow for above indicator', 
        pos=[None, icng.w_shape[1]*0.35], 
        color=COLORS['black'], 
        font=usr.font2, 
        font_size=icng.server_menu_shadow, 
        window_shape=usr.w_shape, 
        show=False
    ),
    interface.centered_indicator(
        text='Hosting server at bla bla', 
        pos=[None, icng.w_shape[1]*0.34], 
        color=COLORS['antiquewhite1'], 
        font=usr.font, 
        font_size=icng.main_menu_fsize, 
        window_shape=usr.w_shape, 
        show=False
    ),
]

all_to_be_drawn = text+levers+indicators