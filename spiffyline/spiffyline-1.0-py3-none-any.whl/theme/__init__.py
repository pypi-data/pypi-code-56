
# trinity John 3:16
# subpackage for providing terminal formatting

import os
import ctypes
import inspect

from ctypes import windll
from .exceptions import VT100Error

# Enable VT-100 terminal emulation for windows users
if os.name == "nt":

    try:

        # Declare aliases

        c_int32 = ctypes.c_int32
        c_ulong = ctypes.c_long

        kernel32 = windll.kernel32

        GetConsoleMode = kernel32.GetConsoleMode

        # Set up functions

        GetConsoleMode.argtypes = [ ctypes.c_void_p, ctypes.POINTER( c_ulong ), ]

        # Get console handle

        STD_OUTPUT_HANDLE = c_int32( -11 )
        
        hOut = kernel32.GetStdHandle( STD_OUTPUT_HANDLE )
        
        # Get current mode

        dwCurrentMode = c_ulong( 0 )
        lpCurrentMode = ctypes.pointer( dwCurrentMode )

        GetConsoleMode( hOut, lpCurrentMode )

        kernel32.SetConsoleMode( hOut, c_ulong( dwCurrentMode.value | 0x0004 ) )
    
    except OSError:
        raise VT100Error()

class Theme( str ):
    """Class the represents formatting options"""

    # Private class variables
    _FG_COLOR_PREFIX = "38;2;"
    _BG_COLOR_PREFIX = "48;2;"

    # Constructors

    
    def __new__( cls, codes, off=None ):
        """
        Creates new Theme from ANSI SGR codes.
        This constructor should not be used
        directly.
        """

        obj = super().__new__( cls, "\u001b[" + codes + "m" )
        
        obj.codes = codes
        obj.off = off

        return obj
    
    @classmethod
    def fg_color( cls, r, g, b ):
        """
        Creates new foreground color Theme from 
        RGB color values.

        Arguments:

        r - red color value (0-255)
        g - green color value (0-255)
        b - blue color value (0-255)
        """

        return cls.__new__( cls, f"{cls._FG_COLOR_PREFIX}{r};{g};{b}", "\u001b[39m" )

    @classmethod
    def bg_color( cls, r, g, b ):
        """
        Creates new background color Theme from 
        RGB color values.

        Arguments:

        r - red color value (0-255)
        g - green color value (0-255)
        b - blue color value (0-255)
        """

        return cls.__new__( cls, f"{cls._BG_COLOR_PREFIX}{r};{g};{b}", "\u001b[49m" )

    # Utility methods

    @classmethod
    def supported_formats( cls ):
        """
        Print names of format options with associated formatting to show suppport
        """

        for i in inspect.getmembers( Theme, lambda a: type( a ) == Theme ):
            print( i[1] + i[0] + ( i[1].off if i[1].off else "" ) )

# Formatting Options

# Text Style
Theme.RESET = Theme( "0" )
Theme.BOLD = Theme( "1", "\u001b[22m" )
Theme.DIM = Theme( "2", "\u001b[22m" )
Theme.ITALIC = Theme( "3", "\u001b[23m" )
Theme.UNDERLINE = Theme( "4", "\u001b[24m"  )
Theme.SLOW_BLINK = Theme( "5", "\u001b[25m" )
Theme.RAPID_BLINK= Theme( "6", "\u001b[25m" )
Theme.INVERT = Theme( "7", "\u001b[27m" )
Theme.CONCEAL = Theme( "8", "\u001b[28m" )
Theme.STRIKE = Theme( "9", "\u001b[29m" )
Theme.DEFAULT_FONT = Theme( "10" )
Theme.ALT_FONT_1 = Theme( "11" )
Theme.ALT_FONT_2 = Theme( "12" )
Theme.ALT_FONT_3 = Theme( "13" )
Theme.ALT_FONT_4 = Theme( "14" )
Theme.ALT_FONT_5 = Theme( "15" )
Theme.ALT_FONT_6 = Theme( "16" )
Theme.ALT_FONT_7 = Theme( "17" )
Theme.ALT_FONT_8 = Theme( "18" )
Theme.ALT_FONT_9 = Theme( "19" )
Theme.FRAKTUR = Theme( "20",  "\u001b[23m"  )
Theme.DEFAULT_FG_COLOR = Theme( "39" )
Theme.DEFAULT_BG_COLOR = Theme( "49" )
Theme.FRAMED = Theme( "51", "\u001b[54m" )
Theme.ENCIRCLED = Theme( "52", "\u001b[54m" )
Theme.OVERLINED = Theme( "53", "\u001b[55m" )
Theme.SUPERSCRIPT = Theme( "73" )
Theme.SUBSCRIPT = Theme( "74" )

# Foreground colors

#Theme.FG_ = Theme.fg_color( )

Theme.FG_WHITE = Theme.fg_color( 255, 255, 255 )
Theme.FG_SILVER = Theme.fg_color( 192, 192, 192 )
Theme.FG_GRAY = Theme.fg_color( 128, 128, 128 )
Theme.FG_BLACK = Theme.fg_color( 0, 0, 0 )
Theme.FG_RED = Theme.fg_color( 255, 0, 0 )
Theme.FG_MAROON = Theme.fg_color( 128, 0, 0 )
Theme.FG_YELLOW = Theme.fg_color( 255, 255, 0 )
Theme.FG_LIME = Theme.fg_color( 0, 255, 0 )
Theme.FG_OLIVE = Theme.fg_color( 128, 128, 0 )
Theme.FG_GREEN = Theme.fg_color( 0, 128, 0 )
Theme.FG_AQUA = Theme.fg_color( 0, 255, 255 )
Theme.FG_TEAL = Theme.fg_color( 0, 128, 128 )
Theme.FG_BLUE = Theme.fg_color( 0, 0, 255 )
Theme.FG_NAVY = Theme.fg_color( 0, 0, 128 )
Theme.FG_PINK = Theme.fg_color( 255, 0, 255 )
Theme.FG_PURPLE = Theme.fg_color( 128, 0, 128 )

# Background colors
Theme.BG_WHITE = Theme.bg_color( 255, 255, 255 )
Theme.BG_SILVER = Theme.bg_color( 192, 192, 192 )
Theme.BG_GRAY = Theme.bg_color( 128, 128, 128 )
Theme.BG_BLACK = Theme.bg_color( 0, 0, 0 )
Theme.BG_RED = Theme.bg_color( 255, 0, 0 )
Theme.BG_MAROON = Theme.bg_color( 128, 0, 0 )
Theme.BG_YELLOW = Theme.bg_color( 255, 255, 0 )
Theme.BG_LIME = Theme.bg_color( 0, 255, 0 )
Theme.BG_OLIVE = Theme.bg_color( 128, 128, 0 )
Theme.BG_GREEN = Theme.bg_color( 0, 128, 0 )
Theme.BG_AQUA = Theme.bg_color( 0, 255, 255 )
Theme.BG_TEAL = Theme.bg_color( 0, 128, 128 )
Theme.BG_BLUE = Theme.bg_color( 0, 0, 255 )
Theme.BG_NAVY = Theme.bg_color( 0, 0, 128 )
Theme.BG_PINK = Theme.bg_color( 255, 0, 255 )
Theme.BG_PURPLE = Theme.bg_color( 128, 0, 128 )
