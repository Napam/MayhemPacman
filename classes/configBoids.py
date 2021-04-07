""" written by Joel
    file from previous assignment with some changes to fit the new one
    contains all the magic numbers for the boid class created in the Pacman game
"""
import numpy as np

# if True the objects that passes through the screen will 
# appear on a random spot on the other side.
RANDOM_MODE = False

# screen settings
SCREEN_WIDTH = 1080
SCREEN_HIGHT = 720
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HIGHT)

FPS = 30
BACKGROUNG_COLOR_MIN = 15
BACKGROUNG_COLOR_MAX = 75

# characters settings
# maxSpeed, color, position, radius, width, hight
BOID_SPEC = (10, (255,255,55), 5, 20,10)
MIN_BOIDFLOCK = 2

COLLITION_RADIUS = 20
FLOCK_RADIUS = 80
PREADATOR_RADIUS = 150

# maxSpeed, color, position, radius, width, hight
PACMAN_SPEC = (15, (255,255,255), 15, 20,10)
PACMAN_START_POS = (500,500)
PACMAN_SIGHT = 250

GHOST_SPEC = (5 , (255,255,255), 50, 20,10)
GHOST_START_POS = [(100,100),(100,700),(700,100),(700,700)]
GHOST_DAMPING = 0.5

# color,  radius, width, hight
OBSTACLE_SPEC = ((255,55,55), 25, 50, 50)
