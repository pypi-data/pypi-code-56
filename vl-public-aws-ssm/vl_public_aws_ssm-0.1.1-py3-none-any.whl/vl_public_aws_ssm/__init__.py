
def load_config(_ssm, path):
    configuration = {}
    
    # Get all parameters for this app
    param_details = _ssm.get_parameters_by_path(
        Path=path, 
        Recursive=False,
        WithDecryption=True
    )

    # Loop through the returned parameters and populate the ConfigParser
    if 'Parameters' in param_details and len(param_details.get('Parameters')) > 0:
        for param in param_details.get('Parameters'):
            param_path_array = param.get('Name').split("/")
            if( len(param_path_array) == 3 ):# Only get first level of configuration items 0 == '', 1 == path, 2 == key
                configuration[param_path_array[2]] = param.get('Value')
        
    return configuration

#TODO : add the load json cfg method?