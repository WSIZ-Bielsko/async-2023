from dataclasses import dataclass
from datetime import date, datetime
from uuid import uuid4, UUID

from loguru import logger
from random import seed

from pydantic import BaseModel

seed(111)


def list_ops():
    a_list = [1, 2, 3, 4]
    a_list.append(11)  # O(1)
    a_list.append(1)
    a_list.remove(1)  # O(N)
    a_list.append(5)
    logger.info(f'My list {a_list}')
    logger.info(f'is 5 in list? {5 in a_list}')  # O(N)


def set_ops():
    a_set = {1, 2, 3, 4}
    a_set.add(11)  # O(1)
    a_set.add(1)  # changes nothing
    a_set.add(5)
    a_set.remove(1)  # O(1)
    logger.info(f'my set: {a_set}')
    logger.info(f'is 5 in set? {5 in a_set}')  # O(1)


# @dataclass
class User(BaseModel):
    uid: UUID
    name: str
    birthdate: date


def containers():
    # list_ops()
    # set_ops()
    user_id = uuid4()
    print(user_id)
    # 15 September 1946
    p_of_zimbabwe = User(uid=uuid4(), name='Mnangagwa', birthdate=date(year=1946, month=9, day=15))
    print(datetime.strftime(p_of_zimbabwe.birthdate, '%Y-%b-%d'))

    presidents: dict[UUID, User] = dict()
    presidents[p_of_zimbabwe.uid] = p_of_zimbabwe  # add --> O(1)

    # May 31, 1962
    p_peru = User(uid=uuid4(), name='Boluarte', birthdate=date(year=1962, month=5, day=31))
    presidents[p_peru.uid] = p_peru

    # Complexities for dict:
    # add, pop (remove), access: d[key], exists? 'Duda' in presidents ? ---> O(1)

    p_of_buthan = User(uid=uuid4(), name='Jigme Khesar', birthdate=date(year=1980, month=2, day=21))
    presidents[p_of_buthan.uid] = p_of_buthan

    logger.info(presidents)

    # różnica wieku...
    dt = p_of_zimbabwe.birthdate - p_peru.birthdate
    print(type(dt))
    print(dt.days)

    # additional structure to find users by name
    user_by_name: dict[str, set[UUID]] = dict()
    for p in presidents.values():
        if p.name not in user_by_name:
            user_by_name[p.name] = set()
        user_by_name[p.name].add(p.uid)

    logger.info(user_by_name['Boluarte'])
    uids = user_by_name['Boluarte']
    for uid in uids:
        logger.warning(presidents[uid])

    print('-----------')
    pp_s = p_peru.json()
    print(type(pp_s))
    zz = User.parse_raw(pp_s)
    logger.warning(zz)
    logger.warning(zz == p_peru)    # comparing by values
    logger.warning(id(zz))
    logger.warning(id(p_peru))

if __name__ == '__main__':
    containers()
