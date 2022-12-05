"""Coffee machines module."""
from dataclasses import dataclass, field
from typing import Literal

from . data_classes import (CoffeeTypes, AutoAmericano, AutoEspresso, AutoCappucino, AutoLatte, 
                         CarobAmericano, CarobCappucino, CarobEspresso, CarobLatte, CoffeeMachines)

class Machine:
    """General class for all cofeemashines."""


@dataclass
class CarobCoffeeMachine(Machine):
    """Automatic coffee machine class."""
    # Container sizes
    MAX_COFFEE: int = 50
    MAX_WATER: int = 500
    MAX_MILK: int = 0

    # Current source values
    COFFEE_VALUE: int = 0
    WATER_VALUE: int = 0
    MILK_VALUE: int = 0
    
    # available drinks
    DRINKS: dict[str, CarobAmericano | CarobEspresso | CarobCappucino | CarobLatte] = field(default_factory=dict)

    @property
    def current_sources(self)->dict[int: int]:
        """Returns current values of source.
            1 - COFFEE
            2 - WATER
            3 - MILK
        """
        return {
            1: self.COFFEE_VALUE,
            2: self.WATER_VALUE,
            3: self.MILK_VALUE
        }

    @property
    def max_sources(self) -> dict[int: int]:
        """Returns max values of source.
            1 - COFFEE
            2 - WATER
            3 - MILK
        """
        return {
            1: self.MAX_COFFEE,
            2: self.MAX_WATER,
            3: self.MAX_MILK
        }


    def add_source(self, source: Literal[1,2,3], source_value: int) -> None:
        """Add selected source.
            1 - COFFEE
            2 - WATER
            3 - MILK
        """
        if source == 1:
            self.COFFEE_VALUE += source_value
        elif source == 2:
            self.WATER_VALUE += source_value
        elif source == 3:
            self.MILK_VALUE += source_value

    def ask_user_for_source(self, source:Literal[1,2,3], need_value: int) -> int:
        """Ask user for needed value of selected source."""
        sources_names_map = {
            1: 'Кофе',
            2: 'Вода',
            3: 'Молоко'
        }

        print(f"В кофемашине закончился ресурс: {sources_names_map[source]}.")
        print("Максимальное значение ресурсов:", self.max_sources)

        while 1:
            source_for_add = input(f"Введите необходимое количество. Минимальное количество {need_value}\n")
            if not source_for_add.isdigit() or int(source_for_add) < need_value:
                print(f"Введено неверное значение ресурса: {sources_names_map[source]}")
                continue
            
            source_for_add=int(source_for_add)
            if source_for_add + self.current_sources[source] > self.max_sources[source]:
                print(f"Введено слишком большое значeние для ресурса {sources_names_map[source]}")
                continue
            
            return source_for_add


    def __validate_sources(self, drink: CarobAmericano | CarobEspresso | CarobCappucino | CarobLatte) -> dict[Literal[1,2,3], int]:
        """Validate all sources for selected coffee drink."""
        coffee_res = drink.COFFEE.value - self.COFFEE_VALUE
        water_res = drink.WATER.value - self.WATER_VALUE
        milk_res = drink.MILK.value - self.MILK_VALUE

        return {
            1: coffee_res,
            2: water_res,
            3: milk_res
        }
    
    def __start_brewing(self, coffee_variant: str, drink: CarobAmericano | CarobEspresso | CarobCappucino | CarobLatte):
        """Start brewing coffee drink."""
        drinks_names_map = {
            '1': 'Эспрессо',
            '2': 'Американо',
            '3': 'Каппучино',
            '4': 'Латте'
        }
        print(f"Начинаем варить ваше {drinks_names_map[coffee_variant]}.")
        self.COFFEE_VALUE -= drink.COFFEE.value
        self.WATER_VALUE -= drink.WATER.value
        self.MILK_VALUE -= drink.MILK.value

        print(f'Ваше {drinks_names_map[coffee_variant]} готово! Наслаждайтесь!')
        print("Отстаток ресурсов:", self.current_sources)

    def brew(self, coffee_variant:str, machine_type:str):
        """Brewing coffee."""
        self.DRINKS = {
            CoffeeTypes.ESPRESSO.value: CarobEspresso,
            CoffeeTypes.AMERICANO.value: CarobAmericano,
            CoffeeTypes.CAPPUCINO.value: CarobCappucino,
            CoffeeTypes.LATTE.value: CarobLatte,
        }

        drink: CarobAmericano | CarobEspresso | CarobCappucino | CarobLatte = self.DRINKS[coffee_variant]
        validation_result: dict[Literal[1,2,3], int] = self.__validate_sources(drink=drink)
        
        for source, result in validation_result.items():
            if result > 0:
                source_value: int = self.ask_user_for_source(source=source, need_value=result)
                self.add_source(source=source, source_value=source_value)
        
        self.__start_brewing(coffee_variant, drink)



@dataclass
class AutoCoffeeMachine(Machine):
    """Automatic coffee machine class."""
    # Container sizes
    MAX_COFFEE: int = 100
    MAX_WATER: int = 500
    MAX_MILK: int = 200

    # Current source values
    COFFEE_VALUE: int = 0
    WATER_VALUE: int = 0
    MILK_VALUE: int = 0
    
    # available drinks
    DRINKS: dict[str, AutoAmericano | AutoEspresso | AutoCappucino | AutoLatte] = field(default_factory=dict)

    @property
    def current_sources(self)->dict[int: int]:
        """Returns current values of source.
            1 - COFFEE
            2 - WATER
            3 - MILK
        """
        return {
            1: self.COFFEE_VALUE,
            2: self.WATER_VALUE,
            3: self.MILK_VALUE
        }

    @property
    def max_sources(self) -> dict[int: int]:
        """Returns max values of source.
            1 - COFFEE
            2 - WATER
            3 - MILK
        """
        return {
            1: self.MAX_COFFEE,
            2: self.MAX_WATER,
            3: self.MAX_MILK
        }


    def add_source(self, source: Literal[1,2,3], source_value: int) -> None:
        """Add selected source.
            1 - COFFEE
            2 - WATER
            3 - MILK
        """
        if source == 1:
            self.COFFEE_VALUE += source_value
        elif source == 2:
            self.WATER_VALUE += source_value
        elif source == 3:
            self.MILK_VALUE += source_value

    def ask_user_for_source(self, source:Literal[1,2,3], need_value: int) -> int:
        """Ask user for needed value of selected source."""
        sources_names_map = {
            1: 'Кофе',
            2: 'Вода',
            3: 'Молоко'
        }

        print(f"В кофемашине закончился ресурс: {sources_names_map[source]}.")
        print("Максимальное значение ресурсов:", self.max_sources)

        while 1:
            source_for_add = input(f"Введите необходимое количество. Минимальное количество {need_value}\n")
            if not source_for_add.isdigit() or int(source_for_add) < need_value:
                print(f"Введено неверное значение ресурса: {sources_names_map[source]}")
                continue
            
            source_for_add=int(source_for_add)
            if source_for_add + self.current_sources[source] > self.max_sources[source]:
                print(f"Введено слишком большое значeние для ресурса {sources_names_map[source]}")
                continue
            
            return source_for_add


    def __validate_sources(self, drink: AutoAmericano | AutoEspresso | AutoCappucino | AutoLatte) -> dict[Literal[1,2,3], int]:
        """Validate all sources for selected coffee drink."""
        coffee_res = drink.COFFEE.value - self.COFFEE_VALUE
        water_res = drink.WATER.value - self.WATER_VALUE
        milk_res = drink.MILK.value - self.MILK_VALUE

        return {
            1: coffee_res,
            2: water_res,
            3: milk_res
        }
    
    def __start_brewing(self, coffee_variant: str, drink: AutoAmericano | AutoEspresso | AutoCappucino | AutoLatte):
        """Start brewing coffee drink."""
        drinks_names_map = {
            '1': 'Эспрессо',
            '2': 'Американо',
            '3': 'Каппучино',
            '4': 'Латте'
        }
        print(f"Начинаем варить ваше {drinks_names_map[coffee_variant]}.")
        self.COFFEE_VALUE -= drink.COFFEE.value
        self.WATER_VALUE -= drink.WATER.value
        self.MILK_VALUE -= drink.MILK.value

        print(f'Ваше {drinks_names_map[coffee_variant]} готово! Наслаждайтесь!')
        print("Отстаток ресурсов:", self.current_sources)

    def brew(self, coffee_variant:str, machine_type:str):
        """Brewing coffee."""
        self.DRINKS = {
            CoffeeTypes.ESPRESSO.value: AutoEspresso,
            CoffeeTypes.AMERICANO.value: AutoAmericano,
            CoffeeTypes.CAPPUCINO.value: AutoCappucino,
            CoffeeTypes.LATTE.value: AutoLatte,
        }

        drink: AutoAmericano | AutoEspresso | AutoCappucino | AutoLatte = self.DRINKS[coffee_variant]
        validation_result: dict[Literal[1,2,3], int] = self.__validate_sources(drink=drink)
        
        for source, result in validation_result.items():
            if result > 0:
                source_value: int = self.ask_user_for_source(source=source, need_value=result)
                self.add_source(source=source, source_value=source_value)
        
        self.__start_brewing(coffee_variant, drink)

