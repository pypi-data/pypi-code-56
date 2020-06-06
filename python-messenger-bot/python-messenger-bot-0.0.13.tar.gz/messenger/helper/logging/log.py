import datetime
import logging
import os

logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logging_format, level=logging.INFO)


def create_logger(name, user_id, folder_log):
    logger = logging.getLogger(name)

    user_log = folder_log + user_id + '/log ' + datetime.datetime.now().strftime('%y-%b-%d %H') + '.txt'

    try:
        fh = logging.FileHandler(user_log, 'a+')
    except FileNotFoundError:
        os.makedirs(folder_log + user_id, exist_ok=True)
        fh = logging.FileHandler(user_log, 'a+')

    formatter = logging.Formatter(logging_format)
    fh.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(fh)

    return logger