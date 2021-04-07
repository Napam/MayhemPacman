'''
Module containing the manager class

Written by Naphat Amundsen
'''

class manager:
    '''
    Finite state machine manager/controller
    '''
    def __init__(self, states={}, state_kwargs=None):
        '''
        state_kwargs are keyword arguments necessary for creating new state 
        instances. The state_kwargs are used for "force reloading" states. 
        '''
        self._states = states
        self._states.update({'exit':None, 'previous':None})
        self.state_kwargs = state_kwargs
        self._buffer = [None]

    def update(self, new_states={}):
        '''
        Update manager's state dictionary
        '''
        self._states.update(new_states)


    def get_state(self, key='', cache=True):
        '''
        Returns state addess given its key 
        '''
        # temp is needed to make the 'previous'
        # key work properly
        temp = self._states[key]

        if cache:
            self._buffer.append(self._states[key])
            self._states['previous'] = self._buffer.pop(0)
        return temp


    def reload_state(self, key=''):
        '''
        Do a soft reload using the state's reload method
        '''
        self._states[key].reload()
    

    def force_reload_state(self, key=''):
        '''
        Creates a new instance of the target class if force reload possible
        '''
        try:
            self._states[key] = self._states[key].__class__(self, **self.state_kwargs) 
        except Exception:
            print('Insufficient arguments given to manager, force reload not possible')
    

