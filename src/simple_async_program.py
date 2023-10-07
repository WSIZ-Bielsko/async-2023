# from time import sleep
from asyncio import sleep, run

from loguru import logger

from src.utils import tn


async def work():
    logger.info('async works')
    logger.info(tn())
    await sleep(0.5)
    logger.info('meh; now done')







if __name__ == '__main__':
    logger.info(tn())

    run(work())