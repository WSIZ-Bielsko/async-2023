from asyncio import run, TaskGroup, create_task
from loguru import logger

async def foo(a: int):
    logger.info(f'foo {a=}')


async def main():
    async with TaskGroup() as tg:
        t1 = tg.create_task(foo(5))
        t2 = tg.create_task(foo(6))

    logger.info('tasks complete')


if __name__ == '__main__':
    run(main())