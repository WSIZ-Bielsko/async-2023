from asyncio import run
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

    def __init__(self, ttl: float = 10**9):
        self.s = set()
        # tu stworzyć strukturę, która będzie zapamiętywała która wartość kiedy została wrzucona do self.s
        # niech się nazywa self.value_age

    async def initialize(self):
        # tu uruchomić task, który będzie przeglądał co 0.1 sek self.value_age, i jeśli przekroczy ona self.ttl, to
        # uruchomi self.remove
        pass

    def add(self, item):
        self.s.add(item)

    def remove(self, item):
        self.s.remove(item)

    def __contains__(self, item):
        return item in self.s

    def __repr__(self):
        return self.s.__repr__()

async def main():
    pass


if __name__ == '__main__':
    run(main())

    s = SetTTL()
    s.add(10)
    s.add(11)
    s.add(10)
    print(s)
    print(10 in s)
    s.remove(11)
    print(s)
