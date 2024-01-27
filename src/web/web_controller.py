from platform import node

from aiohttp import web
from loguru import logger

from model import User

routes = web.RouteTableDef()

app_state = dict()
app_state['users'] = dict()  # userid -> user


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
    # app_state['db'].insert_user(user) ...

    users_db = app_state['users']
    if user.id in users_db:
        logger.warning(f'Trying to overwrite existing user with id={user.id}')
        return web.json_response({'result': 'Error: trying to overwrite user with same id', 'host': node()},
                                 status=400)
    users_db[user.id] = user
    return web.json_response(user.__dict__)


@routes.get('/users/{id}')
async def get_user_with_id(request):
    logger.info(f'GET /users hit')
    try:
        user_id = request.match_info['id']
    except RuntimeError:
        return web.json_response({'result': f'User id provided', 'host': node()}, status=400)

    logger.info(f'Getting user with id={user_id}')

    users_db = app_state['users']
    if user_id not in users_db:
        return web.json_response({'result': f'No user id={user_id} exists', 'host': node()}, status=400)

    return web.json_response({'result': users_db[user_id].__dict__, 'host': node()}, status=200)


async def app_factory():
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    i.e. we can initialize database connection here...
    """
    app = web.Application()
    app.add_routes(routes)
    # app_state['db'] = DbService(...)
    return app


if __name__ == '__main__':
    web.run_app(app_factory(), port=5000)
