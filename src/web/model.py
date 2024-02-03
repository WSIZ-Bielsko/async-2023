from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    uid: UUID | None
    name: str
    passwd: str

    def serialized(self):
        self.uid = str(self.uid)
        self.passwd = ''
        return self.__dict__


@dataclass
class FloatResult:
    result: float
    host: str


@dataclass
class RpsCounter:
    calls_done: int
