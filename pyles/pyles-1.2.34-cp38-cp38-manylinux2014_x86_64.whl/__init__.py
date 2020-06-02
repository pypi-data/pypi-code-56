from pyles._C import *
# TODO distinguish protocol files version, teles core library version and python module version
#      we may update codes or add api in python side without modification on C++ side.
from pyles._C import (__version__, __doc__)
from pyles.telesapp import TelesApp
