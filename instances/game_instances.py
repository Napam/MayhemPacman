'''
Module containing the in-game mayhem instances
such as the ship, planets, asteroid objects etc etc...

Written by Naphat Amundsen
'''
import numpy as np
import pygame as pg
import configparser
import sys
import os

sys.path.insert(0,'..')

from classes import spaceship
from classes import planet
from classes import maps
from classes import interface

import user_settings as user_cng
from instances import instance_config as icng

pg.font.init()

w_shape = user_cng.w_shape
w_norm = np.linalg.norm(w_shape)
COLORS = pg.colordict.THECOLORS

# The initial values of the objects 
# are mostly just educated guesses

game_map = maps.game_map(
    map_shape=(icng.map_shape)
)

minimap = maps.minimap(
    gmap=game_map, 
    w_shape=w_shape, 
    w_norm=w_norm)

ship = spaceship.spaceship(
    pos=(200,200),
    init_dir=icng.RIGHT
)

sun = planet.planet(
    pos=game_map.center, 
    init_vel=None, 
    init_dir=None,
    rforce=None
)

earth = planet.rotating_planet(
    pos=(game_map.shape[0]/2, 800), 
    init_vel=[-3,0], 
    init_dir=[1,0],
    r_force=25000,
    omega=0.25
)

venus = planet.rotating_planet(
    pos=(game_map.shape[0]/2, 2000), 
    init_vel=[-5,0], 
    init_dir=[1,0],
    r_force=40000,
    omega=0.25
)

asteroids = [
    planet.rotating_planet(
        pos=(3000, 1000), 
        init_vel=[-8,2], 
        init_dir=[1,0],
        r_force=150000,
        omega=0.25
    ),
    planet.rotating_planet(
        pos=(1200, 1000), 
        init_vel=[10,1], 
        init_dir=[1,0],
        r_force=390000,
        omega=0.25
    ),
    planet.rotating_planet(
        pos=(500, 2000), 
        init_vel=[2,10], 
        init_dir=[1,0],
        r_force=540000,
        omega=0.25
    ),
    planet.rotating_planet(
        pos=(6500, 6000), 
        init_vel=[5,-15], 
        init_dir=[1,0],
        r_force=1500000,
        omega=0.5
    ),
    planet.rotating_planet(
        pos=(6000, 6000), 
        init_vel=[-15,1], 
        init_dir=[1,0],
        r_force=1000000,
        omega=0.5
    ),
    planet.rotating_planet(
        pos=(6000, 500), 
        init_vel=[-8,-2], 
        init_dir=[1,0],
        r_force=600000,
        omega=0.25
    ),
    planet.rotating_planet(
        pos=(5000, 2000), 
        init_vel=[-2,-8], 
        init_dir=[1,0],
        r_force=200000,
        omega=0.25
    ),
    planet.rotating_planet(
        pos=(game_map.shape[0]/2, 800), 
        init_vel=[15,0], 
        init_dir=[1,0],
        r_force=590000,
        omega=0.25
    ),
    planet.rotating_planet(
        pos=(5000, game_map.shape[1]/2), 
        init_vel=[0,10], 
        init_dir=[1,0],
        r_force=150000,
        omega=0.25
    ),
]

# For convenience
planets = [earth, venus]
all_celestials = planets + asteroids

minimap_colors = [
    COLORS['white'],
    COLORS['orange'],
    COLORS['blue'],
    COLORS['green']
]

minimap_sizes = [
    1, 
    int(500/5000*minimap.shape[0]),
    int(250/5000*minimap.shape[0]),
    1
]


'''Minimap stuff for LAN-mayhem'''
minimap_colors_online = [
    COLORS['white'],
    COLORS['orange'],
    COLORS['blue'],
    COLORS['green'],
    COLORS['red'],
]

minimap_sizes_online = [
    1, 
    int(500/5000*minimap.shape[0]),
    int(250/5000*minimap.shape[0]),
    1,
    3
]

