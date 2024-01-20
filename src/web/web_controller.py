from datetime import datetime
from platform import node

from aiohttp import web
from loguru import logger

routes = web.RouteTableDef()

data = dict()


def ts() -> float:
    return datetime.now().timestamp()


@routes.get('/')
async def hello(request):
    logger.info(f'/ path hit on host {node()}')
    return web.json_response({'comment': f'hello from {node()}; nice to answer your call!'})


@routes.get('/add')
async def hello(request):
    summand_a = float(request.rel_url.query.get('a', '2'))
    summand_b = float(request.rel_url.query.get('b', '2'))
    result = summand_a + summand_b
    return web.json_response({'result': result, 'host': node()})


async def app_factory():
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    i.e. we can initialize database connection here...
    """
    app = web.Application()
    app.add_routes(routes)
    # data['db'] = DbService(...)
    return app


if __name__ == '__main__':
    web.run_app(app_factory(), port=5000)
