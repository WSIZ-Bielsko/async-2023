from asyncio import run, sleep
from loguru import logger

from src.weather_service.streets import Street, SnowSweeper


class WeatherService:
    """
    Random weather conditions over the city
    """

    def __init__(self):
        self.name = 'Polyanna'
        self.current_snow_fall_rate = 0

    async def initialize(self):
        logger.info('Service weather initializing')
        while True:
            await sleep(1)
            # update self.current_snow_fall_rate

    async def get_current_snow_fall_rate(self):
        return self.current_snow_fall_rate


class StreetMonitoringService:
    """
    Monitors city CCTV cameras periodically, and updates snow cover for each of the streets of self.city
    """

    def __init__(self, city: dict[str, Street], weather: WeatherService):
        self.current_snow_fall_rate = 0

    async def initialize(self):
        logger.info('Street monitoring initializing')
        while True:
            await sleep(0.5)
            await self.update_street_snow_cover()

    async def update_street_snow_cover(self):
        # use self.weather + some small random variations
        # update snow cover for each of the streets of self.city
        pass


class SnowSweeperDispatcher:

    def __init__(self, city: dict[str, Street], sweepers: list[SnowSweeper]):
        self.sweepers = sweepers
        self.city = city

    async def initialize(self):
        logger.info('Dispatcher initializing')
        while True:
            await sleep(0.5)
            await self.check_city_dispatch_sweeper()

    async def check_city_dispatch_sweeper(self):
        # check if some streets are _really_ under snow
        # if so -- check if some dispatcher is in length=None
        # launch self.dispatch_to_sweep_street()
        pass

    async def dispatch_to_sweep_street(self, street: Street, sweeper: SnowSweeper):

        cover = street.snow_cover_cm
        street.snow_cover_cm = 0
        logger.info(f'sweeper {sweeper.id} sweeping {street.name}')
        sweeper.location = street.name

        await sleep(street.length * cover)

        logger.info(f'sweeper {sweeper.id} sweeping {street.name} complete')
        sweeper.location = None



async def main():
    s = Service()
    await s.initialize()


if __name__ == '__main__':
    run(main())
