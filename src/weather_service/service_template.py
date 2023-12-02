from asyncio import run, sleep
from loguru import logger


class Service:

    def __init__(self):
        self.name = 'Polyanna'

    async def initialize(self):
        logger.info('Service initializing')
        while True:
            logger.info('Service going to sleep')
            await sleep(0.1)
            logger.info('Service awakening')


async def main():
    s = Service()
    await s.initialize()


if __name__ == '__main__':
    run(main())
