"""Resolution class which store Resolution information    
"""

from .params import Params


class Resolution(Params):
    def __init__(self, name, params_names, params_values, params_types):
        """Construct resolution with all information
        
        Arguments:
            name: {str} -- name of the kind module used
            params_name: [{str}] -- parameters names of resolution used
            params_values: [{str}] -- parameters values of resolution used
            params_types: [{str}] -- parameters values of resolution used
        """
        self.module = "Resolution"
        self.name = name
        self.params_names = params_names
        self.params_values = params_values
        self.params_types = params_types
