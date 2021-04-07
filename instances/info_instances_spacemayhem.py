'''
Info instances for Naphat's Mayhem

Written by Naphat Amundsen
'''
import pygame as pg 
from instances import instance_config as cng
from classes import interface

COLORS = pg.colordict.THECOLORS

texts = [
    interface.text_center(
        text='Spacemayhem info',
        pos=[None, cng.w_shape[1]*0.05],
        color=COLORS['maroon'],
        font=cng.font,
        font_size=cng.main_menu_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='Control ship with \'WASD\', Hyperjump with \'J\', Shoot with \'Space\'',
        pos=[None, cng.w_shape[1]*0.12],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='Refuel by flying to Venus (red planet), reload ammo by flying to Earth',
        pos=[None, cng.w_shape[1]*0.18],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='How to join server: Assign IPv4 address of host in user-settings.py,',
        pos=[None, cng.w_shape[1]*0.27],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='then press \'Online multiplayer\' in main menu',
        pos=[None, cng.w_shape[1]*0.33],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='How to host server: Assign your IPv4 address in user-settings.py',
        pos=[None, cng.w_shape[1]*0.42],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='then press \'Toggle server\' in server menu',
        pos=[None, cng.w_shape[1]*0.48],
        color=COLORS['beige'],
        font=cng.font,
        font_size=cng.info_fsize,
        window_shape=cng.w_shape
    ),
    interface.text_center(
        text='Press \'Backspace\' to revert to previous state, and \'F4\' to exit',
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
