from asyncio import run, TaskGroup, create_task, sleep, wait
from loguru import logger


async def foo(a: int):
    logger.info(f'foo {a=} initiated')
    await sleep(a * 0.1)
    logger.info(f'foo {a=} complete')


async def main():
    t1 = create_task(foo(5))
    t2 = create_task(foo(6))
    ts = [t1, t2]

    while True:
        if all([t.done() for t in ts]):
            logger.info('all done; exiting')
            break
        logger.info('not yet done, waiting a bit...')
        await sleep(0.05)

    logger.info(f't1: {t1.done()}')
    logger.info(f't2: {t2.done()}')

    # done, pending = await wait([t1,t2])

    # logger.info(f'tasks complete {done=}, {pending=}')


if __name__ == '__main__':
    run(main())
