from time import sleep

from loguru import logger

from src.utils import tn


def work():
    logger.info('works')
    sleep(0.5)
    logger.info(tn())
    logger.info('meh; now done')





if __name__ == '__main__':
    logger.info(tn())
    work()