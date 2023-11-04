import asyncio
from asyncio import run, sleep, create_task

from loguru import logger


async def goo() -> int:
    logger.info('from goo')
    await sleep(0.5)
    return 10


async def foo() -> int:
    logger.info('from foo')
    await sleep(0.5)
    return 12


async def main():
    logger.info('running')
    # val_f = await foo()
    # val_g = await goo()

    tf = create_task(foo())
    tg = create_task(goo())
    val_f, val_g = await asyncio.gather(*[tf, tg])

    logger.info(f'{val_f=} {val_g=}')


if __name__ == '__main__':
    run(main())
