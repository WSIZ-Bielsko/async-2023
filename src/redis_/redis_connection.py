import asyncio
import datetime
from asyncio import run, gather
from datetime import date
from random import randint
from uuid import UUID, uuid4

from loguru import logger
from pydantic import ValidationError
# import aioredis
from redis import asyncio as aioredis
from redis.asyncio import Redis

from basics import User

PASS = 'eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81'
HOST = '10.10.1.200'
# HOST = 'localhost'


async def save_user(redis: Redis, u: User):
    key = f"user:{u.uid}"
    val = u.json()
    await redis.set(key, val)


async def get_user(redis: Redis, uid: UUID) -> User | None:
    key = f"user:{uid}"
    s_val = await redis.get(key)
    # check if it exists...
    try:
        user = User.parse_raw(s_val)
    except ValidationError:
        return None
    return user


async def create_random_users(redis: Redis, n_users: int):
    names = [randint(10 ** 6, 10 ** 7 - 1) for _ in range(n_users)]
    bdate = date(1970, 1, 1)
    users = [User(uid=uuid4(), name=f'user{u}', birthdate=bdate) for u in names]

    data = dict()
    for u in users:
        key = f'user:{u.uid}'
        val = u.json()
        data[key] = val


    # tasks = [asyncio.create_task(save_user(redis, u)) for u in users]
    tasks = [asyncio.create_task(redis.mset(data))]
    st = datetime.datetime.now().timestamp()
    # todo: try using pipeline
    logger.info(f'tasks for {n_users} users creation launched')
    await gather(*tasks)
    en = datetime.datetime.now().timestamp()
    logger.info(f'tasks for {n_users} users creation complete; {en - st:.3f}s')


async def main():
    logger.info('connection start')
    try:
        redis = await aioredis.from_url(f'redis://:{PASS}@{HOST}',
                                        encoding="utf-8",
                                        decode_responses=True,
                                        max_connections=9000)
    except ConnectionError:
        logger.error('Cannot connect to DB')
        return -1
    logger.info('connection success')

    await redis.sadd('user:1', 'g99')
    zz = await redis.get('pi')
    logger.info(type(zz))
    logger.info(zz)
    # await create_random_users(redis, n_users=1000000)  # 2

    # for i in range(20001):
    #     loop.create_task(go(redis))  # F&F
    # redis.close()
    # await redis.wait_closed()

    # przykład zapisywania userów
    # u = User(uid=uuid4(), name='Orban', birthdate=date(1960, 2, 12))
    # logger.warning(u)
    # await save_user(redis, u)

    # przykład odczytywania userów
    u1 = await get_user(redis, UUID('6c717803-e7df-43c7-802d-bb31310b95a3'))
    logger.warning(u1)


if __name__ == '__main__':
    run(main())
