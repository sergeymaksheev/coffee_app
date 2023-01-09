"""Coffee machines module."""
import itertools
from dataclasses import dataclass
from typing import Literal

from app.classes.data_classes import CoffeeTypes, CoffeeDrink


class Machine:
    """General class for all cofeemashines."""
 
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
    
    def ask_user_for_source(self, source: Literal[1,2,3], need_value: int) -> None:
        """Ask user for needed value of selected source."""
        print(self.source_names)
        current_source = self.source_names[source]
        print(f"В кофемашине закончился ресурс: {current_source}.")
        print("Максимальное значение ресурсов в кофемашине:", self.max_sources)
        print("Отстаток ресурсов:", self.current_sources)

        for _ in itertools.count():
            source_for_add = input(f"Введите необходимое количество. Минимальное количество {need_value}\n")
            if not source_for_add.isdigit() or int(source_for_add) < need_value:
                print(f"Введено неверное значение ресурса: {current_source}")
                continue
            
            source_for_add=int(source_for_add)
            if source_for_add + self.current_sources[source] > self.max_sources[source]:
                print(f"Введено слишком большое значeние для ресурса {current_source}")
                continue
            
            return source_for_add

    def brew(self, coffee_variant:str):
        """Brewing coffee."""
        drink: CoffeeDrink = self.DRINKS[coffee_variant]
        validation_result: dict[Literal[1,2,3], float] = self.validate_sources(drink=drink)
        
        for source, result in validation_result.items():
            if result > 0:
                source_value: int = self.ask_user_for_source(source=source, need_value=result)
                self.add_source(source=source, source_value=source_value)
        
        self.start_brewing(coffee_variant, drink)

    def start_brewing(self, *args, **kwargs):
        raise NotImplementedError()

    def validate_sources(self,  *args, **kwargs):
        raise NotImplementedError()


@dataclass
class CarobCoffeeMachine(Machine):
    """Carob coffee machine class."""
    # Container sizes
    MAX_COFFEE: int = 50
    MAX_WATER: int = 500
    MAX_MILK: int = 0

    # Current source values
    COFFEE_VALUE: int = 0
    WATER_VALUE: int = 0
    MILK_VALUE: int = 0
    
    def __init__(self, drink_class: CoffeeDrink):
        self.DRINKS = {
            CoffeeTypes.ESPRESSO.value: drink_class(milk=0, water=100, coffee=50),
            CoffeeTypes.AMERICANO.value: drink_class(milk=0, water=350, coffee=50),
            CoffeeTypes.CAPPUCINO.value: drink_class(milk=0, water=400, coffee=50),
            CoffeeTypes.LATTE.value: drink_class(milk=0, water=400, coffee=50),
        }

    @property
    def current_sources(self)->dict[int: int]:
        """Returns current values of source.
            1 - COFFEE
            2 - WATER
        """
        return {
            1: self.COFFEE_VALUE,
            2: self.WATER_VALUE
        }

    @property
    def max_sources(self) -> dict[int: int]:
        """Returns max values of source.
            1 - COFFEE
            2 - WATER
        """
        return {
            1: self.MAX_COFFEE,
            2: self.MAX_WATER
        }

    @property
    def source_names(self):
        return {
            1: 'Кофе',
            2: 'Вода'
        }

    def validate_sources(self, drink: CoffeeDrink) -> dict[Literal[1,2,3], float]:
        """Validate all sources for selected coffee drink."""
        coffee_res = drink.coffee - self.COFFEE_VALUE
        water_res = drink.water - self.WATER_VALUE

        return {
            1: coffee_res,
            2: water_res
        }
    
    def start_brewing(self, coffee_variant: str, drink: CoffeeDrink):
        """Start brewing coffee drink."""
        drinks_names_map = {
            '1': 'Эспрессо',
            '2': 'Американо',
            '3': 'Каппучино',
            '4': 'Латте'
        }
        print(f"Начинаем варить ваше {drinks_names_map[coffee_variant]}.")
        self.COFFEE_VALUE -= drink.coffee
        self.WATER_VALUE -= drink.water

        print(f'Ваше {drinks_names_map[coffee_variant]} готово! Наслаждайтесь!')
        print("Отстаток ресурсов:", self.current_sources)



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

    def __init__(self, drink_class: CoffeeDrink):
        self.DRINKS = {
            CoffeeTypes.ESPRESSO.value: drink_class(milk=0, water=50, coffee=50),
            CoffeeTypes.AMERICANO.value: drink_class(milk=0, water=250, coffee=50),
            CoffeeTypes.CAPPUCINO.value: drink_class(milk=150, water=100, coffee=50),
            CoffeeTypes.LATTE.value: drink_class(milk=200, water=50, coffee=50),
        }


    @property
    def source_names(self):
        return {
            1: 'Кофе',
            2: 'Вода',
            3: 'Молоко'
        }


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

    def validate_sources(self, drink: CoffeeDrink) -> dict[Literal[1,2,3], int]:
        """Validate all sources for selected coffee drink."""
        coffee_res = drink.coffee - self.COFFEE_VALUE
        water_res = drink.water - self.WATER_VALUE
        milk_res = drink.milk - self.MILK_VALUE

        return {
            1: coffee_res,
            2: water_res,
            3: milk_res
        }
    
    def start_brewing(self, coffee_variant: str, drink: CoffeeDrink):
        """Start brewing coffee drink."""
        drinks_names_map = {
            '1': 'Эспрессо',
            '2': 'Американо',
            '3': 'Каппучино',
            '4': 'Латте'
        }
        print(f"Начинаем варить ваше {drinks_names_map[coffee_variant]}.")
        self.COFFEE_VALUE -= drink.coffee
        self.WATER_VALUE -= drink.water
        self.MILK_VALUE -= drink.milk

        print(f'Ваше {drinks_names_map[coffee_variant]} готово! Наслаждайтесь!')
        print("Отстаток ресурсов:", self.current_sources)
    

@dataclass
class CapsuleCoffeeMachine(Machine):
    """Capsule coffee machine class."""

    # Container sizes
    MAX_COFFEE: int = 0
    MAX_WATER: int = 500
    MAX_MILK: int = 0

    # Current source values
    COFFEE_VALUE: int = 0
    WATER_VALUE: int = 0
    MILK_VALUE: int = 0
    
    def __init__(self, drink_class: CoffeeDrink):
        self.DRINKS = {
            CoffeeTypes.ESPRESSO.value: drink_class(milk=0, water=50, coffee=0),
            CoffeeTypes.AMERICANO.value: drink_class(milk=0, water=250, coffee=0),
            CoffeeTypes.CAPPUCINO.value: drink_class(milk=0, water=250, coffee=0),
            CoffeeTypes.LATTE.value: drink_class(milk=0, water=350, coffee=0),
        }

    @property
    def source_names(self):
        return {
            1: 'Вода',
        }

    def add_source(self, source: Literal[1,2,3], source_value: int) -> None:
            """Add selected source.
                1 - WATER
            """
            if source == 1:
                self.WATER_VALUE += source_value

    @property
    def current_sources(self)->dict[int: int]:
        """Returns current values of source.
            1 - WATER
        """
        return {
            1: self.WATER_VALUE
        }

    @property
    def max_sources(self) -> dict[int: int]:
        """Returns max values of source.
            1 - WATER
        """
        return {
            1: self.MAX_WATER
        }


    def validate_sources(self, drink: CoffeeDrink) -> dict[Literal[1,2,3], int]:
        """Validate all sources for selected coffee drink."""
        water_res = drink.water - self.WATER_VALUE

        return {
            1: water_res
        }
    
    def start_brewing(self, coffee_variant: str, drink: CoffeeDrink):
        """Start brewing coffee drink."""
        drinks_names_map = {
            '1': 'Эспрессо',
            '2': 'Американо',
            '3': 'Каппучино',
            '4': 'Латте'
        }
        print(f"Начинаем варить ваше {drinks_names_map[coffee_variant]}.")
        self.WATER_VALUE -= drink.water

        print(f'Ваше {drinks_names_map[coffee_variant]} готово! Наслаждайтесь!')
        print("Отстаток ресурсов:", self.current_sources)
