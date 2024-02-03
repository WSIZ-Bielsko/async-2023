import os
from asyncio import run
from uuid import UUID

import asyncpg
from dotenv import load_dotenv
from loguru import logger

from model import User
from pass_service import PasswordService

load_dotenv()  # take environment variables from .env.

DEFAULT_DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'

DATABASE_URL = os.getenv('DB_URL', DEFAULT_DATABASE_URL)


class DbService:

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
        self.pass_service = PasswordService()

    async def initialize(self):
        try:
            self.pool = await asyncpg.create_pool(self.database_url,
                                                  min_size=5, max_size=10,
                                                  timeout=30, command_timeout=5)
            logger.info('database connected!')
        except Exception as e:
            logger.error(f'Error connecting to DB, {e}')

    async def get_users(self, offset=0, limit=500) -> list[User]:
        logger.info('fetching all users')
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from users order by name offset $1 limit $2', offset, limit)
        logger.info('fetching all users complete')
        users = [User(**dict(r)) for r in rows]
        return users

    async def get_user_by_uid(self, user_id: UUID) -> User | None:
        logger.info(f'fetching user {user_id}')
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from users where uid=$1', user_id)
        logger.info('fetching user complete')
        if not rows:
            return None
        return User(**dict(rows[0]))


    async def create(self, user: User) -> User | None:
        user.passwd = self.pass_service.get_hash(user.passwd)

        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('insert into users(name, passwd) VALUES ($1, $2) returning *',
                                            user.name, user.passwd)
        return User(**dict(row))

    async def remove_user(self, user_id: UUID):
        logger.info(f'user {user_id} removing')
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('delete from users where uid=$1 returning *', user_id)
        logger.info(f'user {user_id} removed')


async def main():
    db = DbService(DATABASE_URL)
    await db.initialize()
    u = await db.create(User(None, 'Atomek1', 'Kadabra'))
    u1 = await db.get_user_by_uid(u.uid)
    print(u1)
    await db.remove_user(u.uid)


if __name__ == '__main__':
    # print(DATABASE_URL)
    run(main())
