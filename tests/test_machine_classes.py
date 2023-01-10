'''tests_for_machine_classes_module'''
from typing import Literal
import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, call
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


@pytest.fixture(name='add_source_capsule_mock')
def add_source_capsule_fixture(mocker: MockerFixture)->MagicMock:
    mock = MagicMock()
    mocker.patch('app.classes.machine_classes.CapsuleCoffeeMachine.add_source', mock)
    return mock


class MachineClassMixin:      

    @pytest.mark.parametrize("coffee_variant", [('1'), ('2'), ('3'),('4'),])
    def test_brew_enough_sources(
        self,
        validate_sources_mock:MagicMock,
        ask_user_for_source_mock:MagicMock,
        add_source_mock:MagicMock,
        start_brewing_mock:MagicMock,
        coffee_variant:str,
    )->None:
        mock_returns = {
            CarobCoffeeMachine: {1: -1.0, 2: -1.0},
            CapsuleCoffeeMachine: {1: -1.0},
            AutoCoffeeMachine: {1: -1.0, 2: -1.0, 3: -1.0},
        }
        validate_sources_mock.return_value = mock_returns[self.TEST_CLASS.__class__]
        self.TEST_CLASS.brew(coffee_variant)
        ask_user_for_source_mock.assert_not_called()
        add_source_mock.assert_not_called()
        start_brewing_mock.assert_called_once_with(coffee_variant, self.TEST_CLASS.DRINKS[coffee_variant])


    @pytest.mark.parametrize("coffee_variant", [('1'), ('2'), ('3'), ('4')])
    def test_brew_not_enough_sources(
        self,
        validate_sources_mock:MagicMock,
        ask_user_for_source_mock:MagicMock,
        add_source_mock:MagicMock,
        start_brewing_mock:MagicMock,
        add_source_capsule_mock: MagicMock,
        coffee_variant:str,
    )->None:
        source_value =  10.0
        ask_user_for_source_mock.return_value = source_value
        mock_returns = {
            AutoCoffeeMachine: {1: 10.0, 2: 10.0, 3: 10.0},
            CarobCoffeeMachine: {1: 10.0, 2: 10.0},
            CapsuleCoffeeMachine: {1: 10.0},
        }
        ask_user_for_source_calls = {
            AutoCoffeeMachine: [call(source=1, need_value=10), call(source=2, need_value=10), call(source=3, need_value=10)],
            CarobCoffeeMachine: [call(source=1, need_value=10), call(source=2, need_value=10)],
            CapsuleCoffeeMachine: [call(source=1, need_value=10)]
        }
        add_source_calls = {
            AutoCoffeeMachine: [
                call(source=1, source_value=source_value), 
                call(source=2, source_value=source_value), 
                call(source=3, source_value=source_value),
            ],
            CarobCoffeeMachine: [
                call(source=1, source_value=source_value), 
                call(source=2, source_value=source_value),
            ],
            CapsuleCoffeeMachine: [call(source=1, source_value=source_value),]
        }
        validate_sources_mock.return_value = mock_returns[self.TEST_CLASS.__class__]
        self.TEST_CLASS.brew(coffee_variant)
        ask_user_for_source_mock.assert_has_calls(ask_user_for_source_calls[self.TEST_CLASS.__class__])
        if self.TEST_CLASS.__class__ == CapsuleCoffeeMachine:
            add_source_capsule_mock.assert_has_calls(add_source_calls[self.TEST_CLASS.__class__])
        else:
            add_source_mock.assert_has_calls(add_source_calls[self.TEST_CLASS.__class__])
        start_brewing_mock.assert_called_once_with(coffee_variant, self.TEST_CLASS.DRINKS[coffee_variant])
        

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