# from time import sleep
import asyncio
from asyncio import sleep

from loguru import logger

from src.utils import thread_name, task_name


async def work(work_id: int):
    logger.info(f'---- starting work with id={work_id}')
    logger.info(thread_name() + "/" + task_name())
    await sleep(0.5)
    logger.info('---- finishing task of function "work"')


async def main1():
    logger.info(f'Starting main1, {thread_name()} / {task_name()}')
    t1 = asyncio.create_task(work(1))
    t2 = asyncio.create_task(work(2))

    await t1
    await t2




if __name__ == '__main__':
    logger.info("starting program, " + thread_name())
    asyncio.run(main1())  # tu program czeka na zakonczenie wykonania funkcji o nazwie `main1`; uruchamia mechanizm asynchroniczny

    logger.info("finishing program, " + thread_name())
