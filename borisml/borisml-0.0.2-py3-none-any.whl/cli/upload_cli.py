# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to upload your embeddings to
    our platform.
    
"""

import hydra

# EXAMPLE FILE
def _upload_cli(cfg):
    print(cfg.pretty())

#@hydra.main(config_file='path/to/config/file')
def upload_cli(cfg):
    _upload_cli(cfg)

def entry():
    upload_cli(cfg)