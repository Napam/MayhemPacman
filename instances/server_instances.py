'''
Module containing instances for server.py 

This module is necessary, since server.py could
not handle some imports propery (server.py will
effectively be run in a different working directory
during runtime)

Written by Naphat Amundsen
'''

from classes import server_state_adapter
from instances import game_instances as game_i
from instances import instance_config as cng

celestial_state_adapter = server_state_adapter.server_game_state(
    game_i.maps.game_map(cng.map_shape)
)