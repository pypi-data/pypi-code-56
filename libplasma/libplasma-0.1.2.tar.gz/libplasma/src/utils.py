#!/usr/bin/env python3

import json
import os

def setup_plasma_directory():
    home_path = os.path.expanduser('~')
    plasma_path = os.path.join(home_path,'.plasma')
    if not os.path.exists(plasma_path):
        os.mkdir(plasma_path)
        config = {}
        config_file_path = os.path.join(plasma_path,"plasma.json")
        with open(config_file_path,'w') as config_file:
            json.dump(config, config_file)
        os.mkdir(os.path.join(plasma_path,'datasets'))
        os.mkdir(os.path.join(plasma_path,'models'))
        os.mkdir(os.path.join(plasma_path,'components'))

def get_plasma_directory():
    home_path = os.path.expanduser('~')
    plasma_path = os.path.join(home_path,'.plasma')
    return plasma_path

def get_config():
    home_path = os.path.expanduser('~')
    safecam_path = os.path.join(home_path,'.plasma')
    config_file_path = os.path.join(safecam_path,'plasma.json')
    with open(config_file_path,'r') as config_file:
        config = json.load(config_file)
    return config

def write_config(config):
    home_path = os.path.expanduser('~')
    safecam_path = os.path.join(home_path,'.plasma')
    config_file_path = os.path.join(safecam_path,'plasma.json')
    with open(config_file_path,'w') as config_file:
        json.dump(config, config_file)

