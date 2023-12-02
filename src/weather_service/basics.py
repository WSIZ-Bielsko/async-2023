from dataclasses import dataclass
from uuid import UUID


@dataclass
class Street:
    name: str
    length: float
    snow_cover_cm: float


@dataclass
class SnowSweeper:
    id: UUID
    name: str
    location: str | None


if __name__ == '__main__':
    s = Street('Cieszyńska', 2.41, snow_cover_cm=0.4)
    c = Street('Krakowska', 3.12, snow_cover_cm=0.2)

    print(s)
    print(s.name)
    s.snow_cover_cm += 1.1
    print(s)

    d = dict()
    d[1] = 12
    d['cieszynska'] = s
    d['zywiecka'] = c

    for k in d.keys():
        print('k---->', d[k])

    for (k, v) in d.items():
        print(k, ' *** ', v)
