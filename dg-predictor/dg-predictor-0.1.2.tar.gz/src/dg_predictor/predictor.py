# -*- coding: utf-8 -*-
"""
predict pipeline
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import logging
import importlib
import yaml
from easydict import EasyDict as edict


__all__ = ['main', 'load_config', 'create_predictor']


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cfg', default=None, type=str, help='yaml config file')
    parser.add_argument('--version', dest='version', action='store_true', help='print version')
    args = parser.parse_args()
    if args.version:
        import dg_predictor as ap
        print("dg-predictor %s" % ap.__version__)
        import sys; sys.exit()
    if args.cfg is None:
        print("Usage: dg-predictor --cfg [yaml config file]")
        import sys; sys.exit()
    return args


def load_config(config_file):
    """
    load yaml config
    """
    with open(config_file, 'r') as f:
        config = edict(yaml.load(f.read(), Loader=yaml.SafeLoader))
    return config


def create_predictor(config):
    """
    create predictor list from config.
    """
    predictors = list()
    for name in config:
        module = "dg_predictor_%s" % name
        predictor_module = importlib.import_module(module)
        predictor_inst = predictor_module.create(config[name])
        predictors.append(predictor_inst)
    return predictors


def main():
    args = parse_args()
    config = load_config(args.cfg)
    predictors = create_predictor(config)
    for predictor in predictors:
        predictor.run()
    logging.info('Done!')


if __name__ == "__main__":
    main()
