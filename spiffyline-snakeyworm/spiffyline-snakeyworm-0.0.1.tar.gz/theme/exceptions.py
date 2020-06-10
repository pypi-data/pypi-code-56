
# Raised when VT-100 can't be enabled
class VT100Error( Exception ):
    def __init__( self ):
        super().__init__( "Couldn't enable VT-100 terminal emulation" )
