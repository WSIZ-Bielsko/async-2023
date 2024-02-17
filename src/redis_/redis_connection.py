from asyncio import run
from datetime import date
from uuid import UUID, uuid4

from loguru import logger
# import aioredis
from redis import asyncio as aioredis
from redis.asyncio import Redis

from basics import User

PASS = 'eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81'


async def save_user(redis: Redis, u: User):
    key = f"user:{u.uid}"
    val = u.json()
    await redis.set(key, val)


async def get_user(redis: Redis, uid: UUID) -> User | None:
    key = f"user:{uid}"
    s_val = await redis.get(key)
    # check if it exists...
    user = User.parse_raw(s_val)
    return user


async def main():
    logger.info('connection start')
    redis = await aioredis.from_url(f'redis://:{PASS}@localhost', encoding="utf-8", decode_responses=True)
    logger.info('connection success')

    await redis.sadd('user:1', 'g99')
    zz = await redis.get('pi')
    logger.info(type(zz))
    logger.info(zz)

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
