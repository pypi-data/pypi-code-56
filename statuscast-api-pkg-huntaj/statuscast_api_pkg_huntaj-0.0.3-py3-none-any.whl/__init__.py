from .StatusCastAPIDriver import StatusCastAPIDriver

# Create the driver
# That will 1) parse the arguments passed to the module, 2) set config variables with passed config filepath
# 3) initialize an authorized session using an auth token
driver = StatusCastAPIDriver()