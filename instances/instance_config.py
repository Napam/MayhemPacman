'''
Module containing instance configurations (and also surface instances)

Written by Naphat Amundsen
'''
import numpy as np
import user_settings as cng

w_shape = np.array(cng.w_shape)
w_norm = np.linalg.norm(w_shape)
norm_square_vec = np.array([w_norm, w_norm])

'''General'''
LEFT = [-1,0]
RIGHT = [1,0]
UP = [0,-1]
DOWN = [0,1]

'''Map'''
map_shape = (7000, 7000)

'''Font'''
font = cng.font
mayhem_title_fsize = int(w_norm * 0.037) 
main_menu_fsize = int(w_norm * 0.025)
server_menu_shadow = int(main_menu_fsize*1.00001)
game_indicator_fsize = int(w_norm*0.015)
game_over_fsize = int(w_norm*0.04)

info_fsize = int(w_norm * 0.02)

''' Image shapes '''
menu_img_shape = w_shape
ship_img_shape = (80,60)
bullet_img_shape = (40, 40)
sun_img_shape = (1000, 1000)
earth_img_shape = (400, 400)
venus_img_shape = (300, 300)
asteroid_img_shape = (120, 120)