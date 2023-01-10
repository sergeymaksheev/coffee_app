"""Dataclasses module."""

from dataclasses import dataclass
from enum import Enum


class CoffeeDrink:
    def __init__(self, milk:float, coffee: float, water: float):
        self.__milk: float = milk
        self.__coffee: float = coffee
        self.__water: float = water

    @property
    def milk(self):
        return self.__milk

    @property
    def coffee(self):
        return self.__coffee

    @property
    def water(self):
        return self.__water


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
class CapsuleTypes(EnumAsList, str, Enum):
    ESPRESSO = '1'
    AMERICANO = '2'
    CAPPUCINO = '3'
    LATTE = '4'


@dataclass
class CoffeeMachines(EnumAsList, str, Enum):
    AUTO = '1'
    CAROB = '2'
    CAPSULE = '3'




