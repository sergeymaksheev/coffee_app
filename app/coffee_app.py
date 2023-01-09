"""Coffee app module."""
import itertools
from .classes.data_classes import CoffeeDrink, CoffeeTypes, CoffeeMachines, CapsuleTypes
from .classes.machine_classes import AutoCoffeeMachine, CarobCoffeeMachine, CapsuleCoffeeMachine


def run_dialog(enum_class: CoffeeMachines | CapsuleTypes | CoffeeTypes, input_text: str, print_text:str):
    for _ in itertools.count():
        input_value: str = input(input_text)
        if input_value in enum_class.as_list():
            return input_value
        print(print_text)


def start_coffee_app() -> None:
    """Coffee application."""
    coffee_machine_classes = {
        '1': AutoCoffeeMachine(drink_class=CoffeeDrink),
        '2': CarobCoffeeMachine(drink_class=CoffeeDrink),
        '3': CapsuleCoffeeMachine(drink_class=CoffeeDrink)
    }

    for _ in itertools.count():
        machine_type = run_dialog(
            enum_class = CoffeeMachines,
            input_text = "Выберите кофемашину: 1 - Автоматическая, 2 - Рожковая, 3 - Капсульная\n", 
            print_text = "Выбрана неверная кофемашина!",
        )    

        if machine_type == CoffeeMachines.CAPSULE.value:
            coffee_variant = run_dialog(
                enum_class = CapsuleTypes,
                input_text = "Выберите капсулу: 1 - Эспрессо, 2 - Американо, 3 - Каппучино, 4 - Латте\n", 
                print_text = "Выбрана неверная капсула!",
            )
        else:
            coffee_variant = run_dialog(
                enum_class = CoffeeTypes,
                input_text = "Выберите напиток: 1 - Эспрессо, 2 - Американо, 3 - Каппучино, 4 - Латте\n",
                print_text = "Выбран неверный напиток!",
            )

        coffee_machine_classes[machine_type].brew(coffee_variant=coffee_variant)
    

#start_coffee_app()

