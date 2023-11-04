# from time import sleep
import asyncio
from asyncio import sleep

from loguru import logger

from src.utils import thread_name, task_name


async def work(work_id: int, wait_time_ms: float):
    logger.info(f'---- starting work with id={work_id}')
    await sleep(0)
    logger.info(thread_name() + "/" + task_name())
    await sleep(wait_time_ms)
    logger.info(f'---- finishing task of function "work", id={work_id}')


async def zegarek(tick_time_ms: float):
    logger.info(f'Starting zegarek on task: {task_name()}')
    click_n = 1
    while True:
        logger.info(f'Zekarek ticks click={click_n}')
        click_n += 1
        await sleep(tick_time_ms)

    logger.info(f'Finishing zegarek on task: {task_name()}')


async def main1():
    logger.info(f'Starting main1, {thread_name()} / {task_name()}')
    t_z = asyncio.create_task(zegarek(0.1))
    t1 = asyncio.create_task(work(1, 0.9))
    t2 = asyncio.create_task(work(2, 0.1))
    t3 = asyncio.create_task(work(3, 0.2))

    await t1
    logger.info("ok T1's has now finished, I can continue to wait for T2's result")
    await t2
    await t3


if __name__ == '__main__':
    logger.info('starting program, ' + thread_name())
    asyncio.run(main1())
    # tu program czeka na zakonczenie wykonania funkcji o nazwie `main1`; uruchamia mechanizm asynchroniczny

    logger.info("finishing program, " + thread_name())
