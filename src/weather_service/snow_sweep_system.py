import random
from asyncio import run, sleep, create_task
from loguru import logger

from streets import Street, SnowSweeper, create_city


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
            self.current_snow_fall_rate = abs(random.gauss()) * 10
            logger.info(f'updated global snow cover rate to {await self.get_current_snow_fall_rate():.1f}')

    async def get_current_snow_fall_rate(self):
        return self.current_snow_fall_rate


class StreetMonitoringService:
    """
    Monitors city CCTV cameras periodically, and updates snow cover for each of the streets of `self.city`
    """

    def __init__(self, city: dict[str, Street], weather: WeatherService):
        self.weather = weather
        self.city = city
        self.current_snow_fall_rate = 0

    async def initialize(self):
        logger.info('Street monitoring initializing')
        while True:
            await sleep(0.5)
            await self.update_street_snow_cover()
            # add some statistics

    async def update_street_snow_cover(self):
        # use self.weather + some small random variations
        # update snow cover for each of the streets of self.city
        current_global_snow_fall_rate = await self.weather.get_current_snow_fall_rate()
        values = []
        for street in self.city.values():
            street.snow_cover_cm += max(0., current_global_snow_fall_rate + random.gauss())
            values.append(street.snow_cover_cm)

        logger.info(f'updated street snow cover; min:{min(values):.1f}, max:{max(values):.1f}')


class SnowSweeperDispatcher:

    def __init__(self, city: dict[str, Street], sweepers: list[SnowSweeper]):
        self.sweepers = sweepers
        self.city = city
        self.ACTIONABLE_SNOW_COVER = 50    # if >= actionable, sweepers should be dispatched

    async def initialize(self):
        logger.info('Dispatcher initializing')
        while True:
            await sleep(0.5)
            await self.check_city_dispatch_sweeper()

    async def check_city_dispatch_sweeper(self):
        # check if some streets are _really_ under snow
        # if so -- check if some dispatcher is in length=None
        # launch self.dispatch_to_sweep_street()
        print(self.city)
        for street in self.city.values():
            if street.snow_cover_cm > self.ACTIONABLE_SNOW_COVER:
                logger.info(f'Street {street.name} has actionable snow cover; looking for free sweeper')
                # find dispatchable sweeper
                for sweeper in self.sweepers:
                    if sweeper.location is None:
                        create_task(self.dispatch_to_sweep_street(street, sweeper))
                        return
                logger.warning(f'No sweeper found to clean up {street.name}')

    async def dispatch_to_sweep_street(self, street: Street, sweeper: SnowSweeper):
        cover = street.snow_cover_cm
        street.snow_cover_cm = 0
        logger.info(f'sweeper {sweeper.name} sweeping {street.name}')
        sweeper.location = street.name

        await sleep(street.length * cover * 0.1)

        logger.info(f'sweeper {sweeper.name} sweeping {street.name} complete')
        sweeper.location = None


async def main():
    city = create_city()
    sweepers = [SnowSweeper(f'Bulldog{i}', location=None) for i in range(2)]

    weather_svc = WeatherService()
    create_task(weather_svc.initialize())

    monitoring_svc = StreetMonitoringService(city, weather_svc)
    create_task(monitoring_svc.initialize())

    dispatcher_svc = SnowSweeperDispatcher(city=city, sweepers=sweepers)
    create_task(dispatcher_svc.initialize())

    await sleep(10**5)


if __name__ == '__main__':
    run(main())
