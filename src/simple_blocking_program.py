from time import sleep

from loguru import logger

from src.utils import thread_name


def work():
    logger.info('works')
    sleep(0.5)
    logger.info(thread_name())
    logger.info('meh; now done')


if __name__ == '__main__':
    logger.info(thread_name())
    work()
