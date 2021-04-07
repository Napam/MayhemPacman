'''
Module for loading and converting images to pygame surface objects (to be used as singletons)
Needs to be initialized using images.init(pygame display object)
'''
import pygame as pg
import numpy as np
import os 

WINDOW = None

from instances import instance_config as icng

# Get the module namespace, which is the global namespace 
GLOBALS = globals()


def load_and_convert(rel_path, shape):
    img = pg.image.load(rel_path).convert_alpha()
    return pg.transform.scale(img, shape)


def load_imgs():
    # ------------- IMAGES -------------#
    menu_img = load_and_convert('images/menu_bg.png', icng.menu_img_shape)
    ship_img = load_and_convert('images/spaceship1.png', icng.ship_img_shape)
    enemyship_img = load_and_convert('images/enemy3.png', icng.ship_img_shape)
    bullet_img = load_and_convert('images/shot.png', icng.bullet_img_shape)
    bg_img = load_and_convert('images/space.png', icng.map_shape)
    sun_img = load_and_convert('images/sun.png', icng.sun_img_shape)
    earth_img = load_and_convert('images/earth.png', icng.earth_img_shape)
    venus_img = load_and_convert('images/venus.png', icng.venus_img_shape)
    asteroid1_img = load_and_convert('images/asteroid1.png', icng.asteroid_img_shape)
    asteroid2_img = load_and_convert('images/asteroid2.png', icng.asteroid_img_shape)
    asteroid3_img = load_and_convert('images/asteroid3.png', icng.asteroid_img_shape)
    # --------------------------------- #

    asteroid_imgs = [
        asteroid1_img, 
        asteroid1_img, 
        asteroid1_img, 
        asteroid2_img,
        asteroid2_img,
        asteroid2_img, 
        asteroid2_img, 
        asteroid3_img, 
        asteroid3_img
    ]

    # Turn images into module variables
    GLOBALS.update(locals())

def init(WINDOW_MAIN):
    '''
    Appends WINDOW_MAIN (a pygame display object) to global namespace
    and therafter loads and convert the images to pygame display objects.

    The function is necessesary since it seems to be that the Surface.convert_alpha() 
    method will not work without an initialized pygame display object in scope. 
    I think..., at least its something like that.
    '''
    GLOBALS['WINDOW'] = WINDOW_MAIN
    load_imgs()
    