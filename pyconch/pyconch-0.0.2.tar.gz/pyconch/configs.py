"""
All configurations for pyconch
"""


from pytconf.config import Config, ParamCreator


class ConfigDummy(Config):
    """
    Parameters for the symlink install tool
    """
    param = ParamCreator.create_str(
        help_string="This is a param",
    )
