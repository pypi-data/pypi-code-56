
# trinity John 3:16
# subpackage for providing terminal logging

import sys

from ..theme import Theme

class Logger:

    
    def __init__( self ):
        """Initialize logger with empty events dict"""
        self.events = {}

    
    def log( self, msg, theme="", flags=[], end="\n", out=sys.stdout ):
        """
        Log content given to sys.stdout(by default) and apply and
        record any themes given

        Arguments:

        msg   - Message to log
        theme - Theme to be used ("" by default)
        flags - Each flag specified will the cause the corresponding
                events[ flag ] to be incremented by 1 ([] by default)
        end   - String to append to end of log ("\\n" by default)
        out   - Output stream to use (sys.stdout by default )
        """

        for flag in flags:
            self.events[flag] = self.events.get( flag, 0 ) + 1

        out.write( theme + msg + Theme.RESET + end )
