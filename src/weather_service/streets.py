from dataclasses import dataclass
import uuid


@dataclass
class Street:
    name: str
    length: float
    snow_cover_cm: float


@dataclass
class SnowSweeper:
    id: uuid.uuid4()
    name: str
    location: str | None


SS = SnowSweeper(uuid.uuid4(), 'adam', 'Bielsko')

print(SS.id)


def create_city() -> dict[str, Street]:
    s1 = Street('Cieszyńska', 2.41, snow_cover_cm=0.4)
    s2 = Street('Krakowska', 3.12, snow_cover_cm=0.2)
    s3 = Street('Lupiecka', 2.12, snow_cover_cm=0.1)
    s4 = Street('Lutomierska', 6.42, snow_cover_cm=0.3)
    s5 = Street('Piastowska', 3.44, snow_cover_cm=0.5)

    ss = [s1, s2, s3, s4, s5]

    city = dict()
    for steet in ss:
        city[steet.name] = steet
    return city


if __name__ == '__main__':
    city = create_city()
    print(city)

    # print(city['cieszynska'].name)

    ssweeper1 = SnowSweeper(uuid.uuid4(), 'Bulldog1', None)
    print(ssweeper1)
