from asyncio import run, sleep
from dataclasses import dataclass
from datetime import datetime
from random import randint
from uuid import UUID, uuid4
from loguru import logger
from faker import Faker

import asyncpg

DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'


@dataclass
class User:
    uid: UUID | None
    name: str
    email: str


class DbService:

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        try:
            self.pool = await asyncpg.create_pool(self.database_url, timeout=30, command_timeout=5)
            logger.info('connected!')
        except Exception as e:
            logger.error(f'Error connecting to DB, {e}')

    async def get_users(self, offset=0, limit=500) -> list[User]:
        logger.info('fetching all users')
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from pusers order by name offset $1 limit $2', offset, limit)
        logger.info('fetching all users complete')
        return [User(**dict(r)) for r in rows]

    async def create(self, user: User) -> User:
        # if user.uid is N -- new user -- insert; else update user with given user.uid
        logger.info(f'Creating user {user}')
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('insert into pusers(name, email) VALUES ($1, $2) returning *',
                                            user.name, user.email)
        logger.info(f'User {user} created')
        return User(**dict(row))

    async def remove_user(self, user_id: UUID):
        logger.info(f'user {user_id} removing')
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('delete from pusers where uid=$1 returning *', user_id)
            print(row)
        logger.info(f'user {user_id} removed')


class UserService:
    def __init__(self):
        self.faker = Faker()

    async def create_random_users(self, n_users: int):
        return [User(uid=None, name=self.faker.name(), email=self.faker.email()) for _ in range(n_users)]


async def main():
    logger.info('App start')
    db = DbService(DATABASE_URL)
    await db.initialize()
    n = randint(0, 1000)
    await db.create(User(uuid4(), f'Li{n}', f'li{n}@xx.cn'))
    for u in await db.get_users(offset=0):
        print(u)
    await db.remove_user(user_id=UUID('dc302ee2-5d67-460f-8fb3-703c20749fe5'))
    uservice = UserService()
    print(await uservice.create_random_users(n_users=1))
    st = datetime.now().timestamp()
    users = await uservice.create_random_users(n_users=1000)
    for u in users:
        await db.create(u)
    en = datetime.now().timestamp()
    logger.warning(f'Created 1000 users in {en - st}s')  # 1000 userow w 13s (dla ping latency = 6ms)

    # await sleep(1)
    # await db.pool.close()
    # await sleep(1)


if __name__ == '__main__':
    run(main())
