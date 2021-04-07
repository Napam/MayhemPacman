'''
Contains template state class (called "state")

Written by Naphat Amundsen
'''
import pygame 

class state:    
    '''
    Template state class that contains methods and attributes that
    all states share.

    activate()
    update_user_input()
    reload() 
    '''
    def __init__(self, MANAGER, WINDOW):
        self.MANAGER = MANAGER
        self.WINDOW = WINDOW
        self._active = False
        self.next_state = self.MANAGER.get_state(key='previous', cache=False)
        self.clock = pygame.time.Clock()

    def activate(self):
        '''Activates the state by setting self._active = True'''
        self._active = True

    def update_user_input(self):
        '''
        Method to update pygame events and user inputs to the states. 

        User input information is stored as attributes for easy
        reuse of the information throughout the whole class 
        '''
        self.click = False
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.next_state = self.MANAGER.get_state('exit')
                self._active = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_BACKSPACE):
                    self.next_state = self.MANAGER.get_state('previous')
                    self._active = False

                if(event.key == pygame.K_F4):
                    self.next_state = self.MANAGER.get_state('exit')
                    self._active = False
    
        self.kbinput = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pressed()

    def reload(self):
        '''
        A method to ensure compatibility in the state machine (so one can freely use polymorphism)
        Not an abstract method since soft reload method is optional
        '''
        pass

    def change_state_to(self, next_state: str, reload=False):
        '''Method to conveniently change to another state'''
        self.next_state = self.MANAGER.get_state(next_state)
        if reload:
            try:
                self.next_state.reload()
            except:
                pass
        self._active = False
        