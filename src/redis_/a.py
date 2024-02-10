from asyncio import run
from loguru import logger
# import aioredis
from redis import asyncio as aioredis

PASS = 'eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81'


async def main():
    logger.info('connection start')
    redis = await aioredis.from_url(f'redis://:{PASS}@localhost', encoding="utf-8", decode_responses=True)
    logger.info('connection success')


    await redis.sadd('user:1', 'g99')

    # for i in range(20001):
    #     loop.create_task(go(redis))  # F&F
    # redis.close()
    # await redis.wait_closed()


if __name__ == '__main__':
    run(main())
