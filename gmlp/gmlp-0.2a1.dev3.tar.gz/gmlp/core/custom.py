"""
For Customization
"""
 
from __future__ import absolute_import
from gmlp.settings import Settings

class Construct:
    """FEATURE STILL IN DEVELOPMENT!"""
    def __init__(self, settings):
        self.sett = settings
        self.settings = Settings(self.sett, False, False)