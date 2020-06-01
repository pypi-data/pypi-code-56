
import logging

from cowpy import cow


__author__ = "Sean Gillies"
__version__ = '1.2.1'

# Get a logger object using the name of this module. Do not however
# configure this or Python's root logger: the `rio` program, of which
# this is a subcommand, makes the necessary configuration.
logger = logging.getLogger(__name__)

