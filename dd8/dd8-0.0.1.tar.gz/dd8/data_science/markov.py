# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 00:36:18 2020

@author: LIM YUAN QING

Adapted from Hands-on Markov Models with Python

"""

import numpy as np

from dd8 import get_basic_logger, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL
logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

class MarkovChain(object):
    def __init__(self, lst_transition_matrix, lst_states):
        """
        Initialize the MarkovChain instance.
        
        Parameters
        ----------
        lst_transition_matrix : 2-D array
            A 2-D array representing the probabilities of change of state in the
            Markov chain
        lst_states: 1-D array
            An array representing the states of the Markov chain. It needs to be
            in the same order as `lst_transition_matrix`.
        """
        self.transition_matrix = lst_transition_matrix
        self.states = lst_states
        self.__dic_state_to_index = {self.states[index]:index 
                                     for index in range(len(self.states))}
        self.__dic_index_to_state = {index:self.states[index] 
                                        for index in range(len(self.states))}
        
    @property
    def transition_matrix(self):
        return self.__npa_transition_matrix
    
    @transition_matrix.setter
    def transition_matrix(self, lst_transition_matrix):
        self.__npa_transition_matrix = np.atleast_2d(lst_transition_matrix)
            
    @property
    def states(self):
        return self.__lst_states
    
    @states.setter
    def states(self, lst_states):
        self.__lst_states = lst_states
        
    
    def next_state(self, str_current_state):
        """
        Returns the state of the random variable at the next time instance.
        
        Parameters
        ----------
        str_current_state : str
            the current state of the system.
        """
        return np.random.choice(
                self.states, 
                p=self.transition_matrix[self.__dic_state_to_index[str_current_state], :])
    
    def generate_states(self, str_current_state, int_num_to_gen=10):
        """
        Generates the next states of the system.
        
        Parameters
        ----------
        str_current_state : str
            The state of the current random variable
        int_num_to_gen : int
            The number of future states to generate.        
        """
        lst_future_states = []
        for i in range(int_num_to_gen):
            str_next_state = self.next_state(str_current_state)
            lst_future_states.append(str_next_state)
            str_current_state = str_next_state
        return lst_future_states
    

        