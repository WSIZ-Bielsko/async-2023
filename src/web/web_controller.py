import os
from platform import node
from uuid import UUID

from aiohttp import web
from loguru import logger

from model import User
from db_service import DbService, DEFAULT_DATABASE_URL

routes = web.RouteTableDef()

app_state = dict()
app_state['users'] = dict()  # userid -> user


def db() -> DbService:
    return app_state['db']


@routes.get('/')
async def hello(request):
    logger.info(f'/ hit on host {node()}')
    return web.json_response({'comment': f'hello from {node()}; nice to answer your call!'})


# add /greet?name=... ; default: user; greet him


@routes.get('/add')
async def request_with_query_params(request):
    logger.info(f'/add hit')
    try:
        summand_a = float(request.rel_url.query.get('a', '2'))
        summand_b = float(request.rel_url.query.get('b', '2'))
    except ValueError:
        return web.json_response({'result': 'Error: parameters "a" and "b" should be numbers', 'host': node()},
                                 status=400)
    result = summand_a + summand_b
    return web.json_response({'result': result, 'host': node()}, status=200)


@routes.post('/users')
async def upload_user(request):
    logger.info(f'POST /users hit')
    data = await request.json()  # dict
    user = User(**data)
    logger.info(f'Creating user {user}')

    user = await db().create(user)
    logger.info(f'created {user}')

    return web.json_response(user.serialized())


@routes.get('/users/{uid}')
async def get_user_with_id(request):
    logger.info('GET /users/{uid} hit')
    try:
        user_id = UUID(request.match_info['uid'])
    except RuntimeError:
        return web.json_response({'result': f'No user id provided', 'host': node()}, status=400)

    logger.info(f'Getting user with id={user_id}')

    user = await db().get_user_by_uid(user_id)

    if not user:
        return web.json_response({'result': f'No user id={user_id} exists', 'host': node()}, status=400)
    return web.json_response(user.serialized(), status=200)


async def app_factory():
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    i.e. we can initialize database connection here...
    """
    app = web.Application()
    app.add_routes(routes)
    DATABASE_URL = os.getenv('DB_URL', DEFAULT_DATABASE_URL)
    app_state['db'] = DbService(DATABASE_URL)
    await db().initialize()
    return app


if __name__ == '__main__':
    web.run_app(app_factory(), port=5000)
