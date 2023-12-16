import os
import time
from asyncio import run, sleep, create_task, gather
from datetime import datetime

from aiofile import async_open
from loguru import logger


def ts():
    return datetime.now().timestamp()


async def save_data(data: bytes):
    mb = len(data) // 1024 ** 2
    chunk_size = 1 * 1024 ** 2
    n_chunks = len(data) // chunk_size

    logger.info(f'data {mb} save start')
    with open('data.bin', 'wb') as f:
        for i in range(n_chunks):
            logger.info(f'saving chunk no {i}')
            f.write(data[i * chunk_size : (i+1) * chunk_size])
            await sleep(0.001)
    logger.info(f'data {mb} save complete')

async def save_data_aiofile(data: bytes):
    mb = len(data) // 1024 ** 2
    chunk_size = 50 * 1024 ** 2
    n_chunks = len(data) // chunk_size

    logger.info(f'data {mb} save start')

    async with async_open('data.bin', 'wb') as f:
        for i in range(n_chunks):
            logger.info(f'saving chunk {i}')
            await f.write(data[i * chunk_size: (i + 1) * chunk_size])

    logger.info(f'data {mb} save complete')


async def big_job(data: bytes):
    logger.info('big_job starting')
    # await sleep(0)
    # await sleep(0.5)
    # time.sleep(0.5)  # blocking!!
    # await save_data(data)
    await save_data_aiofile(data)
    logger.info('big_job complete')


async def allegro_client_traffic(end_by: float):
    logger.info('client traffic starting')
    client_id = 0
    while True:
        logger.info(f'client {client_id} calling')
        await sleep(0.1)
        logger.info(f'client {client_id} got response')
        client_id += 1
        if ts() > end_by:
            break


async def main():
    data = os.urandom(200 * 1024 ** 2)
    start_time = ts()
    t1 = create_task(big_job(data))
    t2 = create_task(allegro_client_traffic(end_by=start_time + 1))
    await gather(t1, t2)
    logger.info('main complete')


if __name__ == '__main__':
    run(main())
