from asyncio import run, sleep, create_task
from datetime import datetime

from loguru import logger

"""
while True:
    # check all self.value_age
    # gather all that need to be removed
    # remove where needed
    # await asyncio.sleep(0.1)
    pass
"""


class SetTTL:

    def __init__(self, ttl: float = 10 ** 9, add_resets_age=False):
        self.add_resets_age = add_resets_age
        self.s = set()
        self.ttl = ttl

        # tu stworzyć strukturę, która będzie zapamiętywała która wartość kiedy została wrzucona do self.s
        # niech się nazywa self.value_age
        self.value_age = dict()  # todo "any" in python

    async def initialize(self):
        # tu uruchomić task, który będzie przeglądał co 0.1 sek self.value_age, i jeśli przekroczy ona self.ttl, to
        # uruchomi self.remove
        logger.info('setttl - initializing')
        create_task(self.__terminator())

    async def __terminator(self):
        logger.info('terminator started')
        while True:
            logger.info(f'terminating...; elements in set: {len(self.s)}')
            self.__purge()
            await sleep(0.1)

    def __purge(self):
        """Removes all elements from self.s which are older than self.ttl"""
        now = datetime.now().timestamp()
        to_remove = []
        for k,v in self.value_age.items():
            if now - v > self.ttl:
                to_remove.append(k)
        for k in to_remove:
            self.s.remove(k)
            self.value_age.pop(k)

    def add(self, item):
        if item not in self.s or self.add_resets_age:
            self.value_age[item] = datetime.now().timestamp()
        self.s.add(item)

    def remove(self, item):
        self.s.remove(item)
        self.value_age.pop(item)

    def __contains__(self, item):
        return item in self.s

    def __repr__(self):
        return self.s.__repr__()


async def main():
    s = SetTTL()
    await s.initialize()

    s.add(10)
    s.add(11)
    await sleep(0.5)
    s.add(10)
    print(s)
    print(10 in s)
    s.remove(11)
    print(s)
    await sleep(10)


if __name__ == '__main__':
    run(main())
