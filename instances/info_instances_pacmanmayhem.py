'''
Info instances for Joel's Mayhem

Written by Naphat Amundsen
'''
import pygame as pg 
from instances import instance_config as cng
from classes import interface

COLORS = pg.colordict.THECOLORS

texts = [
    interface.text_center(
        text='Pacman cage fight info',
        pos=[None, cng.w_shape[1]*0.05],
        color=COLORS['maroon'],
        font=cng.font,
        font_size=cng.main_menu_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='Player 1 (Yellow): Move with arrow keys, shoot with \'SPACE\'',
        pos=[None, cng.w_shape[1]*0.12],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='Player 2 (Orange): Move with WASD, shoot with \'LCTRL\' ',
        pos=[None, cng.w_shape[1]*0.18],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='Press \'Backspace\' to revert to previous state',
        pos=[None, cng.w_shape[1]*0.66],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
]

# Back button in info state
back_button = interface.decorated_button_change_state(
    text = 'Back', 
    pos = cng.w_shape*[0.02, 0.92], 
    color = COLORS['beige'], 
    color_mouseover = COLORS['cyan'], 
    font=cng.font, 
    font_size=cng.main_menu_fsize, 
    next_state='previous'
)

draw_list = texts + [back_button]
