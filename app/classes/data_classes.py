"""Dataclasses module."""

from dataclasses import dataclass
from enum import Enum


class CoffeeDrink:
    """Class CoffeeDrink"""

    def __init__(self, milk: float, coffee: float, water: float):
        self.__milk: float = milk
        self.__coffee: float = coffee
        self.__water: float = water

    @property
    def milk(self):
        """Milk"""
        return self.__milk

    @property
    def coffee(self):
        """Coffee"""
        return self.__coffee

    @property
    def water(self):
        """Water"""
        return self.__water


class EnumAsList:
    """Class EnumAsList"""

    @classmethod
    def as_list(cls):
        """As list"""
        return list(map(lambda c: c.value, cls))


@dataclass
class CoffeeTypes(EnumAsList, str, Enum):
    """Class CoffeeTypes"""

    ESPRESSO = "1"
    AMERICANO = "2"
    CAPPUCINO = "3"
    LATTE = "4"


@dataclass
class CapsuleTypes(EnumAsList, str, Enum):
    """Class CapsuleTypes"""

    ESPRESSO = "1"
    AMERICANO = "2"
    CAPPUCINO = "3"
    LATTE = "4"


@dataclass
class CoffeeMachines(EnumAsList, str, Enum):
    """Class CoffeeMachines"""

    AUTO = "1"
    CAROB = "2"
    CAPSULE = "3"
