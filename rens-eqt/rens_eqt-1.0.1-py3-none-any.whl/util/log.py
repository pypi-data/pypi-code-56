import logging

level = logging.DEBUG

# create logger
logger = logging.getLogger('eqt')
logger.setLevel(level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(level)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
