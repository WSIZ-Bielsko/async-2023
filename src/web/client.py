import asyncio
from asyncio import sleep
from random import random

import aiohttp
from loguru import logger

from model import User, FloatResult, RpsCounter

URL = 'http://localhost:5000'  # insert url of your server


async def add_numbers():
    a = random()
    b = random()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + f'/add?a={a}&b={b}') as res:
            # odpowiednik http://localhost:5000/add?a=3.30&b=7.30
            if res.status == 200:
                f_res = FloatResult(**(await res.json()))
                logger.info(f_res)
            else:
                logger.warning('Error: ' + str(res.text()))


async def upload_user():
    u = User('xx1', 'Romek')
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + '/upload_user', json=u.__dict__) as res:
            logger.info('user=' + str(await res.json()))


# PERFORMANCE TESTS

async def user_agent(counter: RpsCounter, delay: float = 1.0):
    async with aiohttp.ClientSession() as session:
        while True:
            a = random()
            b = random()
            async with session.get(URL + f'/add?a={a}&b={b}') as res:
                counter.calls_done += 1
                await sleep(delay)


async def supervisor(counter: RpsCounter):
    previous_count = 0
    while True:
        await sleep(1)
        requests_done = counter.calls_done - previous_count
        previous_count = counter.calls_done
        logger.info(f'Running at {requests_done} RPS')


async def performance_test(n_workers: int = 1):
    logger.info('Starting performance test')
    counter = RpsCounter(calls_done=0)
    supervisor_task = asyncio.create_task(supervisor(counter))
    for _ in range(n_workers):
        asyncio.create_task(user_agent(counter, delay=0.1))

    await supervisor_task


async def main():
    # await upload_user()
    await add_numbers()
    # await performance_test(n_workers=1000)


if __name__ == "__main__":
    asyncio.run(main())
