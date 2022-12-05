"""Dataclasses module."""

from dataclasses import dataclass
from enum import Enum


@dataclass
class AutoAmericano(int, Enum):
    COFFEE = 50
    MILK = 0
    WATER = 250


@dataclass
class CarobAmericano(int, Enum):
    COFFEE = 50
    MILK = 0
    WATER = 350


@dataclass
class AutoCappucino(int, Enum):
    COFFEE = 50
    MILK = 150
    WATER = 100


@dataclass
class CarobCappucino(int, Enum):
    COFFEE = 50
    MILK = 0
    WATER = 400


@dataclass
class AutoEspresso(int, Enum):
    COFFEE = 50
    MILK = 0
    WATER = 50


@dataclass
class CarobEspresso(int, Enum):
    COFFEE = 50
    MILK = 0
    WATER = 100


@dataclass
class AutoLatte(int, Enum):
    COFFEE = 50
    MILK = 200
    WATER = 50


@dataclass
class CarobLatte(int, Enum):
    COFFEE = 50
    MILK = 0
    WATER = 400


class EnumAsList:
    @classmethod
    def as_list(cls):
        return list(map(lambda c: c.value, cls))


@dataclass
class CoffeeTypes(EnumAsList, str, Enum):
    ESPRESSO = '1'
    AMERICANO = '2'
    CAPPUCINO = '3'
    LATTE = '4'


@dataclass
class CoffeeMachines(EnumAsList, str, Enum):
    AUTO = '1'
    CAROB = '2'
    CAPSULE = '3'



#print(CoffeeTypes.as_list())