"""
Often used helper functions.
"""
from textwarden import config
import logging

logger = logging.getLogger(__name__)

def cmd_arg_split(msg):
    action = msg.content[len(config.prompt):] #message without prompt
    cmd_arg = action.split(" ", 1)
    command = cmd_arg[0].replace('-', '_')
    argstring = None
    if len(cmd_arg)>1:
        argstring = cmd_arg[1]
    return command, argstring


def id_from_mention(mention):
    if mention.startswith('<@!') and mention.endswith('>'):
        return mention[3:-1]
    else:
        logger.debug('NOT ID:{}|'.format(mention))
        return None

