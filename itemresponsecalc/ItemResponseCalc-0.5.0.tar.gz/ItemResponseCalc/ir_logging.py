"""set up logging formats for ItemResponseCalc package"""

import logging


def setup(log_file):
    """create logging handlers
    :param log_file: string file name for logger FileHandler
    :return: None
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # root_logger.setLevel(logging.DEBUG)
    # NOTE: haq_model.usePool MUST be False, to get desired logging level in Pool-ed sub-modules

    # *** create handlers explicitly, to specify encoding:
    if log_file is not None:
        fh = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter('{asctime} {name} {levelname}: {message}',
                                          style='{',
                                          datefmt='%Y-%m-%d %H:%M:%S')
                        )
        root_logger.addHandler(fh)

    # --------------------------------- No console log if running on HCALC?
    # NO, just keep the console log anyway; check nohup.out for progress log
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('{asctime} {name}: {message}',
                                           style='{',
                                           datefmt='%H:%M:%S'))
    root_logger.addHandler(console)