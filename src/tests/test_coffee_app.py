"""tests_for_coffee_app_module"""
from typing import Type, Union
from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture
from src.app.classes.data_classes import CoffeeTypes, CoffeeMachines, CapsuleTypes
from src.app.coffee_app import run_dialog, start_coffee_app


@pytest.fixture(name="input_mock")
def input_fixture(mocker: MockerFixture) -> MagicMock:
    """Imput fixture"""
    mock = MagicMock()
    mocker.patch("src.app.coffee_app.input", mock)
    return mock


@pytest.fixture(name="print_mock")
def print_fixture(mocker: MockerFixture) -> MagicMock:
    """Print fixure"""

    mock = MagicMock()
    mocker.patch("src.app.coffee_app.print", mock)
    return mock


@pytest.fixture(name="count_mock")
def count_fixture(mocker: MockerFixture) -> MagicMock:
    """Count fixture"""

    mock = MagicMock(return_value=[1])
    mocker.patch("src.app.coffee_app.itertools.count", mock)
    return mock


@pytest.fixture(name="run_dialog_mock")
def run_dialog_fixture(mocker: MockerFixture) -> MagicMock:
    """Run dialog fixture"""

    mock = MagicMock()
    mocker.patch("src.app.coffee_app.run_dialog", mock)
    return mock


@pytest.fixture(name="capsule_coffee_machine_brew_mock")
def capsule_coffee_machine_brew_fixture(mocker: MockerFixture) -> MagicMock:
    """Capsule coffee machine brew fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.CapsuleCoffeeMachine.brew", mock)
    return mock


@pytest.fixture(name="auto_coffee_machine_brew_mock")
def auto_coffee_machine_brew_fixture(mocker: MockerFixture) -> MagicMock:
    """Auto coffee machine brew fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.AutoCoffeeMachine.brew", mock)
    return mock


@pytest.fixture(name="carob_coffee_machine_brew_mock")
def carob_coffee_machine_brew_fixture(mocker: MockerFixture) -> MagicMock:
    """Carob coffee machine brew fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.CarobCoffeeMachine.brew", mock)
    return mock


@pytest.mark.parametrize(
    "test_enum_class, test_input_value, test_input_text, test_print_text",
    [
        (CoffeeMachines, "8", "test_input", "test_print"),
        (CapsuleTypes, "8", "test_input", "test_print"),
        (CoffeeTypes, "8", "test_input", "test_print"),
    ],
)
def test_run_dialog_error_input_value_testcases(
    input_mock: MagicMock,
    print_mock: MagicMock,
    count_mock: MagicMock,
    test_enum_class: Union[Type[CoffeeMachines], Type[CapsuleTypes], Type[CoffeeTypes]],
    test_input_value: str,
    test_input_text: str,
    test_print_text: str,
) -> None:
    """Test run dialog error input value testcases"""

    input_mock.return_value = test_input_value
    test_result = run_dialog(
        enum_class=test_enum_class,
        input_text=test_input_text,
        print_text=test_print_text,
    )
    count_mock.assert_called_once()
    input_mock.assert_called_once_with(test_input_text)
    print_mock.assert_called_once_with(test_print_text)
    assert test_result is None


@pytest.mark.parametrize(
    "test_enum_class, test_input_value, test_input_text, test_print_text",
    [
        (CoffeeMachines, "1", "test_input", "test_print"),
        (CoffeeMachines, "2", "test_input", "test_print"),
        (CoffeeMachines, "3", "test_input", "test_print"),
        (CapsuleTypes, "1", "test_input", "test_print"),
        (CapsuleTypes, "2", "test_input", "test_print"),
        (CapsuleTypes, "3", "test_input", "test_print"),
        (CapsuleTypes, "4", "test_input", "test_print"),
        (CoffeeTypes, "1", "test_input", "test_print"),
        (CoffeeTypes, "2", "test_input", "test_print"),
        (CoffeeTypes, "3", "test_input", "test_print"),
        (CoffeeTypes, "4", "test_input", "test_print"),
    ],
)
def test_run_dialog_success_input_value_testcases(
    input_mock: MagicMock,
    print_mock: MagicMock,
    count_mock: MagicMock,
    test_enum_class: Union[Type[CoffeeMachines], Type[CapsuleTypes], Type[CoffeeTypes]],
    test_input_value: str,
    test_input_text: str,
    test_print_text: str,
) -> None:
    """Test run dialog success input value testcases"""

    input_mock.return_value = test_input_value
    test_result = run_dialog(
        enum_class=test_enum_class,
        input_text=test_input_text,
        print_text=test_print_text,
    )
    count_mock.assert_called_once()
    input_mock.assert_called_once_with(test_input_text)
    print_mock.assert_not_called()
    assert test_result == test_input_value


@pytest.mark.parametrize(
    "coffee_machine, coffee_type",
    [
        ("1", "1"),
        ("1", "2"),
        ("1", "3"),
        ("1", "4"),
        ("2", "1"),
        ("2", "2"),
        ("2", "3"),
        ("2", "4"),
        ("3", "1"),
        ("3", "2"),
        ("3", "3"),
        ("3", "4"),
    ],
)
def test_start_coffee_app_machine_success(
    count_mock: MagicMock,
    run_dialog_mock: MagicMock,
    auto_coffee_machine_brew_mock: MagicMock,
    carob_coffee_machine_brew_mock: MagicMock,
    capsule_coffee_machine_brew_mock: MagicMock,
    coffee_machine: str,
    coffee_type: str,
) -> None:
    """Test start coffee app machine success"""
    test_mocks: dict[str, MagicMock] = {
        "1": auto_coffee_machine_brew_mock,
        "2": carob_coffee_machine_brew_mock,
        "3": capsule_coffee_machine_brew_mock,
    }

    run_dialog_mock.side_effect = [coffee_machine, coffee_type]
    start_coffee_app()
    count_mock.assert_called_once()
    test_mocks[coffee_machine].assert_called_once_with(coffee_variant=coffee_type)
