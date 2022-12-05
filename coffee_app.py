"""Coffee app module."""

from classes.data_classes import CoffeeTypes, CoffeeMachines
from classes.machine_classes import AutoCoffeeMachine, CarobCoffeeMachine


def _ask_for_drink() -> str:
    while 1:
        coffee_variant: str = input("Выберите напиток: 1 - Эспрессо, 2 - Американо, 3 - Каппучино, 4 - Латте\n")
        
        if coffee_variant in CoffeeTypes.as_list():
            return coffee_variant
        print("Выбран неверный напиток!")
    
    
def _ask_for_machine_type() -> str:
    while 1:
        coffee_machine: str = input("Выберите кофемашину: 1 - Автоматическая, 2 - Рожковая, 3 - Капсульная\n")
        if coffee_machine in CoffeeMachines.as_list():
            return coffee_machine
        print("Выбрана неверная кофемашина!")


def start_coffee_app() -> None:
    """Coffee application."""
    coffee_machine_classes = {
        '1': AutoCoffeeMachine(),
        '2': CarobCoffeeMachine(),
        #'3': Capsule_coffee_machine
    }

    while 1:
        coffee_variant = _ask_for_drink()
        machine_type = _ask_for_machine_type()
        coffee_machine_classes[machine_type].brew(coffee_variant=coffee_variant, machine_type=machine_type)
    

start_coffee_app()