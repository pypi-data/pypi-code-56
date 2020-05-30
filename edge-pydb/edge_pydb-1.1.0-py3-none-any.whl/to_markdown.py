import os as _os
import json as _json
import shutil as _shutil
import requests as _requests
import markdown


def to_markdown(files, write_to):
    """The function will take a lists of file names and generate a md file"""
    