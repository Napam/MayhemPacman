""" written by Joel	
	all the magic numbers for the Pacman game
"""
import pygame as pg
import numpy as np
import user_settings 

				# GENERAL STUFF
SCREEN_RESOLUTION = np.array(user_settings.w_shape)
BACKGROUND_COLOR = (10,10,10)
FPS = 30

MAX_NUM_BOIDS = 45
DMG_BULLETS = 10
COOLDOWN_BULLET_TRAVEL = 30
RANDOM_MODE = False

				# PACMAN STUFF
# maxSpeed, color, radius, width, hight, angle, position, mass
PACMAN_SPECS_1 = (5, (0,255,0), 35, 10, 20, 0, (SCREEN_RESOLUTION*[.5,.1]).tolist(), 10**1)
KEYS_PLAYER_1 = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_SPACE]


# maxSpeed, color, radius, width, hight, angle, position, mass
PACMAN_SPECS_2 = (5, (255,0,0), 35, 10, 20, 0, (SCREEN_RESOLUTION*[.5,.9]).tolist(), 10**1)
KEYS_PLAYER_2 =	[pg.K_w, pg.K_s, pg.K_a, pg.K_d, pg.K_LCTRL]

PACMAN_LIFE = 100
PACMAN_love = 100
PACMAN_BELLY_SIZE = 15
PACMAN_BOIDS_IN_BELLY = 10

COOLDOWN_SHOOT = 7
COOLDOWN_USE_love = 20

HEAL_RATE = .1
RELOVE_RATE = .3

				# GHOST STUFF
# color, position, radius, width, hight, angle
GHOST_SPECS = (0,0,255), SCREEN_RESOLUTION*[.5,.5], 50, 1, 1, 0, 10**4
MASS_GHOST = 10**5
GHOST_LIFE = 333

				# Ms PACMAN STUFF
# maxSpeed, color, radius, width, hight, angle, position, mass
MsPacman_SPECS = (4, (255,255,0), 15, 10, 20, 0, [650,250],  3*10**3)
MsPacman_ORBIT_RATIUS = 300
MS_PACMAN_ADDS_BOID_COOLDOWN = 60

				# BOID STUFF
# maxSpeed, color, position, radius, width, hight
BOID_SPEC = (10, (255,255,55), 5, 20,10)
MIN_BOIDFLOCK = 2

COLLITION_RADIUS = 20
FLOCK_RADIUS = 80
PREADATOR_RADIUS = 150

				# TEXT STUFF
TEXT_WIN_COLOR_SIZE_POS = [(255,255,255), 50, SCREEN_RESOLUTION*[.35,.1]]
TEXT_RETRY_COLOR_SIZE_POS =[(255,255,255), 40, SCREEN_RESOLUTION*[.3,.65]]

TEXT_SCORE_COLOR_SIZE_POS = [(255,255,255), 50, SCREEN_RESOLUTION*[.45,.95]]

TEXT_LIFE_SIZE_POS_PLAYER1 = [30, SCREEN_RESOLUTION*[.85,.87]]
TEXT_LOVE_SIZE_POS_PLAYER1 = [30, SCREEN_RESOLUTION*[.85,.91]]
TEXT_BOIDS_SIZE_POS_PLAYER1 = [30, SCREEN_RESOLUTION*[.85,.95]]

TEXT_LIFE_SIZE_POS_PLAYER2 = [30, SCREEN_RESOLUTION*[.05,.87]]
TEXT_LOVE_SIZE_POS_PLAYER2 = [30, SCREEN_RESOLUTION*[.05,.91]]
TEXT_BOIDS_SIZE_POS_PLAYER2 = [30, SCREEN_RESOLUTION*[.05,.95]]




