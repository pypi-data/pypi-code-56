import sys
import inspect

EMPTY = inspect.Parameter.empty

class InspectResult():
    def __init__(self, function):
        sig = inspect.signature(function)
        self.defaults = {}
        self.vararg_key = None

        for param in sig.parameters.values():
            if param.kind == param.POSITIONAL_OR_KEYWORD:
                self.defaults[param.name] = param.default
            
            if param.kind == param.VAR_KEYWORD:
                self.vararg_key = param.name

def get_fn_arg_keys_and_defaults(fn):
    # This limits support to py36
    return InspectResult(fn)

def filter_dict(dict_to_filter, fn):
    function_signature = get_fn_arg_keys_and_defaults(fn)
    filtered_dict = {}
    
    for key, default_value in function_signature.defaults.items():
        value = dict_to_filter.get(key, default_value)
        if value is EMPTY:
            # Missing value for arg without a default value.
            raise KeyError(key)
        else:
            filtered_dict[key] = value
    
    if function_signature.vararg_key:
        # A **kwargs argument is present. We can add the whole dict_to_filter.
        filtered_dict.update(dict_to_filter)
    
    return filtered_dict

class IncrementalModuleError(Exception):
    pass

class IncrementalModuleLoader(object):
    def __init__(self):
        self.modules = dict()
    
    def __getitem__(self, key):
        return self.modules[key]

    def get(self, key, default=None):
        return self.modules.get(key, default)

    def update(self, *args, **kwargs):
        """
        Add an injectable module to the list of modules, without any initialization.
        """
        self.modules.update(*args, **kwargs)

    def _create_module(self, mod):
        try:
            filtered_kwargs = filter_dict(self.modules, mod)
        except KeyError as e:
            raise IncrementalModuleError('Module %s is not loaded, but requested by %s.' % (str(e), mod))
        return mod(**filtered_kwargs)
    
    def load(self, _anonymous_mod=None, **new_modules):
        """
        Dynamically create the modules in arguments with the existing, already loaded
        modules.
        Params:
            _anonymous_mod: Positional argument. If the module is passed without a key,
                it will appear as an 'anonymous' module: the next modules loaded won't 
                have access to it in their dependencies.
            **new_modules: Load A SINGLE module with the current loaded modules as arguments
                and add it to the list of modules under the name specified with each key.
                For multiple modules, call this function once per module.
        Returns:
            The created module.
        """
        if _anonymous_mod is not None and new_modules:
            raise IncrementalModuleError('Either specify the positional module alone, or a single key=module pair.')
        elif _anonymous_mod is not None:
            # Return the anonymous module.
            return self._create_module(_anonymous_mod)
        elif new_modules:
            if len(new_modules) > 1:
                raise IncrementalModuleError('Only call load(key=module) with a single key=module pair.')
            # For loop, but we just checked there is only one key=value pair present.
            # This allows us to return the created module directly in loop.
            for mod_name, fn in new_modules.items():
                if mod_name in self.modules:
                    raise IncrementalModuleError('%s: duplicate module name' % mod_name)
                
                created_module = self._create_module(fn)
                self.modules[mod_name] = created_module
                return created_module