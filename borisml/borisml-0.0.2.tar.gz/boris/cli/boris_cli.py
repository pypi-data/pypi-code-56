# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to embed your image dataset with 
    state-of-the-art technology.

"""


import hydra
import boris

from .train_cli import _train_cli
from .embed_cli import _embed_cli


@hydra.main(config_path="./config/boris_config.yaml", strict=False)
def boris_cli(cfg):
    """ train a self-supervised model and use it to embed your dataset

    Args:
        see train_cli.py, embed_cli.py or
        https://www.notion.so/whattolabel/WhatToLabel-Documentation-28e645f5564a453e807d0a384a4e6ea7

    """

    cfg['loader']['shuffle'] = True
    cfg['loader']['drop_last'] = True
    checkpoint = _train_cli(cfg)

    cfg['loader']['shuffle'] = False
    cfg['loader']['drop_last'] = False
    cfg['checkpoint'] = checkpoint
    _embed_cli(cfg)


def entry():
    boris_cli()

