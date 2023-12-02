from asyncio import sleep
from unittest import IsolatedAsyncioTestCase

from set_with_ttl import SetTTL


class Test(IsolatedAsyncioTestCase):


    def setUp(self):
        # synchronous setup if needed
        pass

    async def asyncSetUp(self):
        # asynchronous setup if needed
        pass

    async def test_simple(self):
        testee = SetTTL()
        await testee.initialize()
        testee.add(12)
        self.assertTrue(12 in testee)

    async def test_removal(self):
        testee = SetTTL()
        await testee.initialize()
        testee.add(12)
        testee.remove(12)
        self.assertTrue(12 not in testee)

    async def test_auto_removal(self):
        testee = SetTTL(ttl=0.1)
        await testee.initialize()
        testee.add(12)
        await sleep(0.3)
        self.assertTrue(12 not in testee)