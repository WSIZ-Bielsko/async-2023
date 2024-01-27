from platform import node

from aiohttp import web
from loguru import logger

from model import User

routes = web.RouteTableDef()

app_state = dict()


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
    # app_state['db'].insert_user(user) ...
    return web.json_response(user.__dict__)


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
