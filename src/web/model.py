from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str


@dataclass
class FloatResult:
    result: float
    host: str


@dataclass
class RpsCounter:
    calls_done: int
