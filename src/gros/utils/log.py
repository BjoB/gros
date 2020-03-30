import logging
import colorlog


def init_logger(module_name):
    log_format = (
        '%(asctime)s - '
        '%(name)s - '
        '%(levelname)s - '
        '%(message)s'
    )
    colorlog_format = (
        '%(log_color)s '
        f'{log_format}'
    )

    colorlog.basicConfig(format=colorlog_format)
    logging.Formatter(log_format)

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    return logger
