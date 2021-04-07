'''
This .py file is just a general template that works well with
the rest of the framework. If you would want to integrate another 
kind of state to the framework, the only requirements are:

The state class (in this template it's "name") needs to have an 
"activate" and "run" method. A reload method is optional.
'''
import sys 
sys.path.insert(0, '..')

import subprocess
import socket
'''
Module containing the server_menu class.

Written by Naphat Amundsen
'''

import pygame as pg
from states import state
import user_settings as cng

from instances import server_menu_instances as menu_i
from instances import info_instances_spacemayhem as info_i
from images import images

import platform

class mock_server_process:
    def poll(self):
        return 1

class server_menu(state.state):
    '''Server menu class, inherits state.state and is meant to be a part of a state machine'''
    def __init__(self, MANAGER, WINDOW):
        super().__init__(MANAGER, WINDOW)
        self.fps = cng.fps/2

        self.run_server = False
        
        # Determines the terminal command for python given the operating system.
        # The server is activated by initializing a separate python interpreter
        # using subprocess.Popen()
        ostype = platform.system()
        if ostype == 'Windows':
            self.python_terminal_command = 'python'
        elif ostype == 'Linux':
            self.python_terminal_command = 'python3'
        elif ostype == 'Darwin':
            self.python_terminal_command = 'python'

        self.server = cng.server if not cng.server == 'host' else socket.gethostbyname(socket.gethostname())
        self.server_process = mock_server_process()

    def update_graphics(self):
        '''
        Blits and flips
        '''
        self.WINDOW.blit(
            images.menu_img,
            (0,0)
        )
        for interface_object in menu_i.all_to_be_drawn:
            interface_object.draw(self.WINDOW)
        
        info_i.back_button.draw(self.WINDOW)

        pg.display.update()

    def interact_user(self):
        '''
        Method for user interactions
        '''
        info_i.back_button.interact_mouse(self.mouse_pos, self.click)
        if info_i.back_button.state:
            self.change_state_to('previous')
        
        if menu_i.levers[0].interact_mouse(self.mouse_pos, self.click):
            self.run_server = not self.run_server
            if self.run_server:
                self.server_process = subprocess.Popen([self.python_terminal_command, 'server.py'], cwd='server') 
            else:
                self.server_process.terminate()
                print('Server stopped')
        
        # To make indicators work if server crashes or gets termibated silently
        # self.server_process.poll() returns None when there is a server running (weird)
        if self.server_process.poll():
            menu_i.levers[0].state = False
            self.run_server = False
    
    def animations(self):
        '''
        Handles animation logic, graphical changes that does not affect anything
        '''
        if not self.server_process.poll():
            menu_i.indicators[0].text_r = f'Hosting LAN server at {self.server} : {cng.port}'
            menu_i.indicators[1].text_r = f'Hosting LAN server at {self.server} : {cng.port}'
            menu_i.indicators[0].show=True
            menu_i.indicators[1].show=True
        else:
            menu_i.indicators[0].show=False
            menu_i.indicators[1].show=False

    def run(self):
        '''
        The "main" loop 
        '''
        while(self._active):
            self.clock.tick(self.fps)
            self.update_user_input()
            self.interact_user()
            self.update_graphics()
            self.animations()
        return self.next_state    
    
    def exit_protocoll(self):    
        '''Terminates server, used in main_class'''
        try:
            self.server_process.terminate()
            print('Terminated server, shutting down')
        except:
            print('No server was terminated, shutting down')