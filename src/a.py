from time import sleep

from loguru import logger

if __name__ == '__main__':
    logger.info('works')
    sleep(0.5)
    logger.info('meh; now done')
