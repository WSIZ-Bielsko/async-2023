from asyncio import run, sleep, create_task
from loguru import logger


async def job():
    logger.info('starting big_job')
    await sleep(0.1)


async def main():
    t = create_task(job())
    await t
    logger.info('main complete')


if __name__ == '__main__':
    run(main())
