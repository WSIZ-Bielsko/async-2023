from asyncio import run, create_task, sleep, gather
from loguru import logger


async def foo(a: int) -> int:
    logger.info(f'foo starting for {a=}')
    await sleep(0.1)
    logger.info('foo complete')
    return a


async def main():
    logger.info('main starting (we are in async world finally -- have event loop)')
    ret1 = await foo(10)  # oczekujemy na wynik działania funkcji foo
    # logger.info(f'main got {ret1=}')
    t1 = create_task(foo(11))
    t2 = create_task(foo(12))
    logger.info('main doing other stuff..')
    z = await gather(t1, t2)    # todo: check if all of them are DONE (but not wait for that...)
    logger.info(f'got {z=}')



if __name__ == '__main__':
    run(main())  # wrzucamy task na event loop
