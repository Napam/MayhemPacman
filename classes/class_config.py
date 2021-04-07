'''
Module containing configuration variables for classes in general

Written by Naphat Amundsen
'''
import numpy as np

''' General '''
LEFT = np.array([-1,0])
RIGHT = np.array([1,0])
UP = np.array([0,-1])
DOWN = np.array([0,1])
sun_center_delete_radius = 500

''' spaceship-ship '''
a_thrust = 0.9
f_drag = 0.04
omega = 0.07

fire_lag = 10
jump_lag = 100
reload_lag = 10

max_fuel = 3000
max_ammo = 50
max_hp = 100

refuel_rate = 5
reload_rate = 1

hyperjump_multiplier = 25
hyperjump_cost = 200

asteroid_collision_radius = 100

inner_planet_gravity_radius = 120

radial_force_constant = 300000

reverse_multiplier = 0.15

bullet_collision_radius = 70
bullet_collision_radius2 = 45

''' Projectile '''
initial_pos_offset = 50
initial_bullet_velocity = 25
bullet_radial_force_constant = radial_force_constant*2

''' Minimap '''
minimap_size = 250 
minimap_pos_multiplier = 0.015
minimap_color = [100, 100, 100]
minmap_alpha = 200
minimap_player_color = [255, 255, 100]
minimap_fov_color = [255, 255, 255]


''' Interface config '''


