import asyncio
from asyncio import create_task, sleep, run
from enum import Enum

from loguru import logger


async def boil_water(arg: str) -> str:
    assert arg == 'water'
    res = 'hot water'
    await sleep(0.1 * len(res))
    return res


async def boil_rice(arg: str) -> str:
    assert arg == 'rice'
    res = 'boiled rice'
    await sleep(0.1 * len(res))
    return res


async def cut_meat(arg: str) -> str:
    assert arg == 'meat'
    res = 'meat pieces'
    await sleep(0.1 * len(res))
    return res


async def cut_coriander(arg: str) -> str:
    assert arg == 'coriander'
    res = 'coriander pieces'
    await sleep(0.1 * len(res))
    return res


async def prepare_sauce(arg: str) -> str:
    assert arg == 'cold sauce'
    res = 'tikka masala sauce'
    await sleep(0.1 * len(res))
    return res


async def prepare_tea(arg: str) -> str:
    logger.info(f'preparing tea with {arg=}')
    assert arg == 'hot water'
    res = 'tea'
    await sleep(0.1 * len(res))
    return res


async def fry_meat(arg: str) -> str:
    logger.info(f'frying meat with {arg=}')
    assert arg == 'meat pieces'
    res = 'fried meat'
    await sleep(0.1 * len(res))
    return res


async def mix_tikka(arg: list[str]) -> str:
    logger.info(f'mixing with {arg=}')
    needed = ['boiled rice', 'fried meat', 'coriander pieces', 'tikka masala sauce']
    for ingr in needed:
        assert ingr in arg
    res = 'tikka masala'
    await sleep(0.1 * len(res))
    return res


async def serve_tikka_masala(arg: list[str]) -> str:
    needed = ['tikka masala', 'tea']
    for ingr in needed:
        assert ingr in arg
    res = 'tikka masala serving'
    await sleep(0.1 * len(res))
    return res


async def full_prepare_tea(arg: str):
    water = await boil_water(arg)
    tea = await prepare_tea(water)
    return tea


async def preparation():
    tea = asyncio.create_task(full_prepare_tea('water'))
    boiled_rice = asyncio.create_task(boil_rice('rice'))
    meat_pieces = asyncio.create_task(cut_meat('meat'))
    coriander = asyncio.create_task(cut_coriander('coriander'))
    sauce = asyncio.create_task(prepare_sauce('cold sauce'))

    boiled_rice, meat_pieces, coriander, sauce = await asyncio.gather(boiled_rice, meat_pieces, coriander, sauce)

    fried_meat = asyncio.create_task(fry_meat(meat_pieces))

    tea, fried_meat = await asyncio.gather(tea, fried_meat)
    tikka = await mix_tikka([boiled_rice, fried_meat, coriander, sauce])

    serving = await serve_tikka_masala([tea, tikka])

    logger.info(f'Prepared: {serving}')


async def main():
    logger.info('running')
    await preparation()


if __name__ == '__main__':
    run(main())
