'''tests_for_machine_classes_module'''
from typing import Literal
import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from app.classes.data_classes import CoffeeDrink
from app.classes.machine_classes import AutoCoffeeMachine, CarobCoffeeMachine, CapsuleCoffeeMachine


@pytest.fixture(name='ask_user_for_source_mock')
def ask_user_for_source_fixture(mocker: MockerFixture)->MagicMock:
    mock = MagicMock()
    mocker.patch('app.classes.machine_classes.Machine.ask_user_for_source', mock)
    return mock


@pytest.fixture(name='add_source_mock')
def add_source_fixture(mocker: MockerFixture)->MagicMock:
    mock = MagicMock()
    mocker.patch('app.classes.machine_classes.Machine.add_source', mock)
    return mock


class MachineClassMixin:      

    @pytest.mark.parametrize("coffee_variant", [('1'),('2'),('3'),('4')])
    def test_brew_enough_sources(
        self,
        validate_sources_mock:MagicMock,
        ask_user_for_source_mock:MagicMock,
        add_source_mock:MagicMock,
        start_brewing_mock:MagicMock,
        coffee_variant:str,
        validate_return_value: dict[Literal[1,2,3], float]
    )->None:
        validate_sources_mock.return_value = validate_return_value
        self.TEST_CLASS.brew(coffee_variant)
        ask_user_for_source_mock.assert_not_called()
        add_source_mock.assert_not_called()
        start_brewing_mock.assert_called_once_with(coffee_variant, self.TEST_CLASS.DRINKS[coffee_variant])
        # return_value={1: -1.0, 2: -1.0, 3: -1.0}


class TestAutoMachine(MachineClassMixin):
    @pytest.fixture(name='validate_sources_mock')
    def validate_sources_fixture(self, mocker: MockerFixture)->MagicMock:
        mock = MagicMock()
        mocker.patch('app.classes.machine_classes.AutoCoffeeMachine.validate_sources', mock)
        return mock

    @pytest.fixture(name='start_brewing_mock')
    def start_brewing_fixture(self, mocker: MockerFixture)->MagicMock:
        mock = MagicMock()
        mocker.patch('app.classes.machine_classes.AutoCoffeeMachine.start_brewing', mock)
        return mock

    TEST_CLASS = AutoCoffeeMachine(drink_class=CoffeeDrink)



class TestCarobMachine(MachineClassMixin):
    @pytest.fixture(name='validate_sources_mock')
    def validate_sources_fixture(self, mocker: MockerFixture)->MagicMock:
        mock = MagicMock()
        mocker.patch('app.classes.machine_classes.CarobCoffeeMachine.validate_sources', mock)
        return mock

    @pytest.fixture(name='start_brewing_mock')
    def start_brewing_fixture(self, mocker: MockerFixture)->MagicMock:
        mock = MagicMock()
        mocker.patch('app.classes.machine_classes.CarobCoffeeMachine.start_brewing', mock)
        return mock

    TEST_CLASS = CarobCoffeeMachine(drink_class=CoffeeDrink)


class TestCapsuleMachine(MachineClassMixin):
    @pytest.fixture(name='validate_sources_mock')
    def validate_sources_fixture(self, mocker: MockerFixture)->MagicMock:
        mock = MagicMock()
        mocker.patch('app.classes.machine_classes.CapsuleCoffeeMachine.validate_sources', mock)
        return mock

    @pytest.fixture(name='start_brewing_mock')
    def start_brewing_fixture(self, mocker: MockerFixture)->MagicMock:
        mock = MagicMock()
        mocker.patch('app.classes.machine_classes.CapsuleCoffeeMachine.start_brewing', mock)
        return mock

    TEST_CLASS = CapsuleCoffeeMachine(drink_class=CoffeeDrink)