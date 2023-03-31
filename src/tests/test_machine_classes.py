"""tests_for_machine_classes_module"""
from typing import Literal
from unittest.mock import MagicMock, call
import pytest
from pytest_mock import MockerFixture
from src.app.classes.data_classes import CoffeeDrink
from src.app.classes.machine_classes import (
    AutoCoffeeMachine,
    CarobCoffeeMachine,
    CapsuleCoffeeMachine,
)


@pytest.fixture(name="count_mock")
def count_fixture(mocker: MockerFixture) -> MagicMock:
    """Count fixture"""

    mock = MagicMock(return_value=[1])
    mocker.patch("src.app.classes.machine_classes.itertools.count", mock)
    return mock


@pytest.fixture(name="print_mock")
def print_fixture(mocker: MockerFixture) -> MagicMock:
    """Print fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.print", mock)
    return mock


@pytest.fixture(name="input_mock")
def input_fixture(mocker: MockerFixture) -> MagicMock:
    """Input fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.input", mock)
    return mock


@pytest.fixture(name="ask_user_for_source_mock")
def ask_user_for_source_fixture(mocker: MockerFixture) -> MagicMock:
    """Ask user for source fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.Machine.ask_user_for_source", mock)
    return mock


@pytest.fixture(name="add_source_mock")
def add_source_fixture(mocker: MockerFixture) -> MagicMock:
    """Add source fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.Machine.add_source", mock)
    return mock


@pytest.fixture(name="add_source_capsule_mock")
def add_source_capsule_fixture(mocker: MockerFixture) -> MagicMock:
    """Add source capsu;e fixture"""

    mock = MagicMock()
    mocker.patch("src.app.classes.machine_classes.CapsuleCoffeeMachine.add_source", mock)
    return mock


class MachineClassMixin:
    """Base test class for common class Macine"""

    TEST_CLASS: AutoCoffeeMachine | CarobCoffeeMachine | CapsuleCoffeeMachine

    @pytest.mark.parametrize(
        "coffee_variant",
        [
            ("1"),
            ("2"),
            ("3"),
            ("4"),
        ],
    )
    def test_brew_enough_sources(
        self,
        validate_sources_mock: MagicMock,
        ask_user_for_source_mock: MagicMock,
        add_source_mock: MagicMock,
        start_brewing_mock: MagicMock,
        coffee_variant: str,
    ) -> None:
        """Test brew enough sources"""
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

    @pytest.mark.parametrize("coffee_variant", [("1"), ("2"), ("3"), ("4")])
    def test_brew_not_enough_sources(
        self,
        validate_sources_mock: MagicMock,
        ask_user_for_source_mock: MagicMock,
        add_source_mock: MagicMock,
        start_brewing_mock: MagicMock,
        add_source_capsule_mock: MagicMock,
        coffee_variant: str,
    ) -> None:
        """Test brew not enough sources"""
        source_value = 10.0
        ask_user_for_source_mock.return_value = source_value
        mock_returns = {
            AutoCoffeeMachine: {1: 10.0, 2: 10.0, 3: 10.0},
            CarobCoffeeMachine: {1: 10.0, 2: 10.0},
            CapsuleCoffeeMachine: {1: 10.0},
        }
        ask_user_for_source_calls = {
            AutoCoffeeMachine: [
                call(source=1, need_value=10),
                call(source=2, need_value=10),
                call(source=3, need_value=10),
            ],
            CarobCoffeeMachine: [call(source=1, need_value=10), call(source=2, need_value=10)],
            CapsuleCoffeeMachine: [call(source=1, need_value=10)],
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
            CapsuleCoffeeMachine: [
                call(source=1, source_value=source_value),
            ],
        }
        validate_sources_mock.return_value = mock_returns[self.TEST_CLASS.__class__]
        self.TEST_CLASS.brew(coffee_variant)
        ask_user_for_source_mock.assert_has_calls(ask_user_for_source_calls[self.TEST_CLASS.__class__])
        if self.TEST_CLASS.__class__ == CapsuleCoffeeMachine:
            add_source_capsule_mock.assert_has_calls(add_source_calls[self.TEST_CLASS.__class__])
        else:
            add_source_mock.assert_has_calls(add_source_calls[self.TEST_CLASS.__class__])
        start_brewing_mock.assert_called_once_with(coffee_variant, self.TEST_CLASS.DRINKS[coffee_variant])

    @pytest.mark.parametrize(
        "coffee_variant",
        [
            ("1"),
            ("2"),
            ("3"),
            ("4"),
        ],
    )
    def test_start_brewing(self, coffee_variant: str, print_mock: MagicMock) -> None:
        """Test start brewing"""
        drink = self.TEST_CLASS.DRINKS[coffee_variant]
        self.TEST_CLASS.start_brewing(coffee_variant=coffee_variant, drink=drink)
        print_mock.assert_called()
        assert print_mock.call_count == 3


class TestAutoMachine(MachineClassMixin):
    """Test class for AutoCoffeeMachine class"""

    TEST_CLASS = AutoCoffeeMachine(drink_class=CoffeeDrink)

    @pytest.fixture(name="validate_sources_mock")
    def validate_sources_fixture(self, mocker: MockerFixture) -> MagicMock:
        """Validate sources fixture"""
        mock = MagicMock()
        mocker.patch("src.app.classes.machine_classes.AutoCoffeeMachine.validate_sources", mock)
        return mock

    @pytest.fixture(name="start_brewing_mock")
    def start_brewing_fixture(self, mocker: MockerFixture) -> MagicMock:
        """Start brewing fixture"""
        mock = MagicMock()
        mocker.patch("src.app.classes.machine_classes.AutoCoffeeMachine.start_brewing", mock)
        return mock

    def teardown(self):
        """Clear values for new test"""
        self.TEST_CLASS.COFFEE_VALUE = 0
        self.TEST_CLASS.WATER_VALUE = 0
        self.TEST_CLASS.MILK_VALUE = 0

    @pytest.mark.parametrize(
        "source, source_value, expected",
        [
            (1, 50.0, 50.0),
            (2, 10.0, 10.0),
            (3, 10.0, 10.0),
            (1, -10.0, 0.0),
        ],
    )
    def test_add_source(
        self,
        source: Literal[1, 2, 3],
        source_value: float,
        expected: float,
    ) -> None:
        """Test add source"""
        self.TEST_CLASS.add_source(source=source, source_value=source_value)

        if source == 1:
            assert self.TEST_CLASS.COFFEE_VALUE == expected
        elif source == 2:
            assert self.TEST_CLASS.WATER_VALUE == expected
        elif source == 3:
            assert self.TEST_CLASS.MILK_VALUE == expected

    @pytest.mark.parametrize(
        "source, need_value, source_for_add",
        [
            (1, 10, "10"),
            (2, 10, "500"),
            (3, 10, "100"),
        ],
    )
    def test_ask_user_for_source_correct_value(
        self,
        source: Literal[1, 2, 3],
        need_value: int,
        count_mock: MagicMock,
        input_mock: MagicMock,
        source_for_add: str,
    ) -> None:
        """Test ask user for source correct value"""
        input_mock.return_value = source_for_add
        result = self.TEST_CLASS.ask_user_for_source(source=source, need_value=need_value)
        count_mock.assert_called_once()
        assert result == float(source_for_add)

    @pytest.mark.parametrize(
        "source, need_value, source_for_add",
        [
            (1, 10, "2000"),
            (2, 10, "9"),
            (3, 10, "string"),
        ],
    )
    def test_ask_user_for_source_wrong_value(
        self,
        source: Literal[1, 2, 3],
        need_value: int,
        count_mock: MagicMock,
        input_mock: MagicMock,
        source_for_add: str,
        print_mock: MagicMock,
    ) -> None:
        """Test ask user for source wrong value"""
        input_mock.return_value = source_for_add
        result = self.TEST_CLASS.ask_user_for_source(source=source, need_value=need_value)
        count_mock.assert_called_once()
        print_mock.assert_called()
        assert print_mock.call_count == 5
        assert result is None

    def test_source_name(self) -> None:
        """Test source name"""
        test_result = {1: "Кофе", 2: "Вода", 3: "Молоко"}
        assert test_result == self.TEST_CLASS.source_names

    @pytest.mark.parametrize(
        "coffee_variant, coffee_value, water_value, milk_value, expected_result",
        [
            ("1", 0, 0, 0, {1: 50, 2: 50, 3: 0}),
            ("1", 10, 10, 10, {1: 40, 2: 40, 3: -10}),
            ("2", 0, 0, 0, {1: 50, 2: 250, 3: 0}),
            ("2", 10, 10, 10, {1: 40, 2: 240, 3: -10}),
            ("3", 0, 0, 0, {1: 50, 2: 100, 3: 150}),
            ("3", 10, 10, 10, {1: 40, 2: 90, 3: 140}),
            ("4", 0, 0, 0, {1: 50, 2: 50, 3: 200}),
            ("4", 10, 10, 10, {1: 40, 2: 40, 3: 190}),
        ],
    )
    def test_validate_sources(
        self,
        expected_result: dict[Literal[1, 2, 3], int],
        coffee_variant: str,
        coffee_value: int,
        water_value: int,
        milk_value: int,
    ) -> None:
        """Test validate sources"""
        self.TEST_CLASS.COFFEE_VALUE = coffee_value
        self.TEST_CLASS.WATER_VALUE = water_value
        self.TEST_CLASS.MILK_VALUE = milk_value
        drink = self.TEST_CLASS.DRINKS[coffee_variant]
        test_result = self.TEST_CLASS.validate_sources(drink=drink)
        assert test_result == expected_result


class TestCarobMachine(MachineClassMixin):
    """Test class for CarobCoffeeMachine class"""

    TEST_CLASS = CarobCoffeeMachine(drink_class=CoffeeDrink)

    @pytest.fixture(name="validate_sources_mock")
    def validate_sources_fixture(self, mocker: MockerFixture) -> MagicMock:
        """Validate sources fixture"""
        mock = MagicMock()
        mocker.patch("src.app.classes.machine_classes.CarobCoffeeMachine.validate_sources", mock)
        return mock

    @pytest.fixture(name="start_brewing_mock")
    def start_brewing_fixture(self, mocker: MockerFixture) -> MagicMock:
        """Start brewing fixture"""
        mock = MagicMock()
        mocker.patch("src.app.classes.machine_classes.CarobCoffeeMachine.start_brewing", mock)
        return mock

    def teardown(self):
        """Clear values for new test"""
        self.TEST_CLASS.COFFEE_VALUE = 0
        self.TEST_CLASS.WATER_VALUE = 0
        self.TEST_CLASS.MILK_VALUE = 0

    @pytest.mark.parametrize(
        "source, source_value, expected",
        [
            (1, 50.0, 50.0),
            (2, 10.0, 10.0),
            (1, -10.0, 0.0),
        ],
    )
    def test_add_source(
        self,
        source: Literal[1, 2, 3],
        source_value: float,
        expected: float,
    ) -> None:
        """Test add source"""
        self.TEST_CLASS.add_source(source=source, source_value=source_value)

        if source == 1:
            assert self.TEST_CLASS.COFFEE_VALUE == expected
        elif source == 2:
            assert self.TEST_CLASS.WATER_VALUE == expected

    @pytest.mark.parametrize(
        "source, need_value, source_for_add",
        [
            (1, 10, "10"),
            (2, 10, "500"),
            (2, 10, "100"),
        ],
    )
    def test_ask_user_for_source_correct_value(
        self,
        source: Literal[1, 2, 3],
        need_value: int,
        count_mock: MagicMock,
        input_mock: MagicMock,
        source_for_add: str,
    ) -> None:
        """Test ask user for source correct value"""
        input_mock.return_value = source_for_add
        result = self.TEST_CLASS.ask_user_for_source(source=source, need_value=need_value)
        count_mock.assert_called_once()
        assert result == float(source_for_add)

    @pytest.mark.parametrize(
        "source, need_value, source_for_add",
        [
            (1, 10, "2000"),
            (2, 10, "9"),
            (2, 10, "string"),
        ],
    )
    def test_ask_user_for_source_wrong_value(
        self,
        source: Literal[1, 2, 3],
        need_value: int,
        count_mock: MagicMock,
        input_mock: MagicMock,
        source_for_add: str,
        print_mock: MagicMock,
    ) -> None:
        """Test ask user for source wrong value"""

        input_mock.return_value = source_for_add
        result = self.TEST_CLASS.ask_user_for_source(source=source, need_value=need_value)
        count_mock.assert_called_once()
        print_mock.assert_called()
        assert print_mock.call_count == 5
        assert result is None

    def test_source_name(self) -> None:
        """Test source name"""

        test_result = {
            1: "Кофе",
            2: "Вода",
        }
        assert test_result == self.TEST_CLASS.source_names

    @pytest.mark.parametrize(
        "coffee_variant, coffee_value, water_value, expected_result",
        [
            ("1", 0, 0, {1: 50, 2: 100}),
            ("1", 10, 10, {1: 40, 2: 90}),
            ("2", 0, 0, {1: 50, 2: 350}),
            ("2", 10, 10, {1: 40, 2: 340}),
            ("3", 0, 0, {1: 50, 2: 400}),
            ("3", 10, 10, {1: 40, 2: 390}),
            ("4", 0, 0, {1: 50, 2: 400}),
            ("4", 10, 10, {1: 40, 2: 390}),
        ],
    )
    def test_validate_sources(
        self, expected_result: dict[Literal[1, 2, 3], int], coffee_variant: str, coffee_value: int, water_value: int
    ) -> None:
        """Test validate sources"""
        self.TEST_CLASS.COFFEE_VALUE = coffee_value
        self.TEST_CLASS.WATER_VALUE = water_value
        drink = self.TEST_CLASS.DRINKS[coffee_variant]
        test_result = self.TEST_CLASS.validate_sources(drink=drink)
        assert test_result == expected_result


class TestCapsuleMachine(MachineClassMixin):
    """Test class for CapsuleCoffeeMachine class"""

    TEST_CLASS = CapsuleCoffeeMachine(drink_class=CoffeeDrink)

    @pytest.fixture(name="validate_sources_mock")
    def validate_sources_fixture(self, mocker: MockerFixture) -> MagicMock:
        """Validate sources fixture"""
        mock = MagicMock()
        mocker.patch("src.app.classes.machine_classes.CapsuleCoffeeMachine.validate_sources", mock)
        return mock

    @pytest.fixture(name="start_brewing_mock")
    def start_brewing_fixture(self, mocker: MockerFixture) -> MagicMock:
        """Start brewing fixture"""
        mock = MagicMock()
        mocker.patch("src.app.classes.machine_classes.CapsuleCoffeeMachine.start_brewing", mock)
        return mock

    def teardown(self):
        """Clear values for new test"""
        self.TEST_CLASS.WATER_VALUE = 0

    @pytest.mark.parametrize(
        "source, source_value, expected",
        [
            (2, 50.0, 50.0),
            (2, -10.0, 0.0),
        ],
    )
    def test_add_source(
        self,
        source: Literal[1, 2, 3],
        source_value: float,
        expected: float,
    ) -> None:
        """Test add source"""
        self.TEST_CLASS.add_source(source=source, source_value=source_value)
        assert self.TEST_CLASS.WATER_VALUE == expected

    @pytest.mark.parametrize(
        "source, need_value, source_for_add",
        [
            (2, 10, "10"),
            (2, 10, "500"),
            (2, 10, "100"),
        ],
    )
    def test_ask_user_for_source_correct_value(
        self,
        source: Literal[1, 2, 3],
        need_value: int,
        count_mock: MagicMock,
        input_mock: MagicMock,
        source_for_add: str,
    ) -> None:
        """Test ask user for source correct value"""
        input_mock.return_value = source_for_add
        result = self.TEST_CLASS.ask_user_for_source(source=source, need_value=need_value)
        count_mock.assert_called_once()
        assert result == float(source_for_add)

    @pytest.mark.parametrize(
        "source, need_value, source_for_add",
        [
            (2, 10, "2000"),
            (2, 10, "9"),
            (2, 10, "string"),
        ],
    )
    def test_ask_user_for_source_wrong_value(
        self,
        source: Literal[1, 2, 3],
        need_value: int,
        count_mock: MagicMock,
        input_mock: MagicMock,
        source_for_add: str,
        print_mock: MagicMock,
    ) -> None:
        """Test ask user for source wrong value"""
        input_mock.return_value = source_for_add
        result = self.TEST_CLASS.ask_user_for_source(source=source, need_value=need_value)
        count_mock.assert_called_once()
        print_mock.assert_called()
        assert print_mock.call_count == 5
        assert result is None

    def test_source_name(self) -> None:
        """Test source name"""
        test_result = {
            2: "Вода",
        }
        assert test_result == self.TEST_CLASS.source_names

    @pytest.mark.parametrize(
        "coffee_variant, coffee_value, expected_result",
        [
            ("1", 0, {2: 50}),
            ("1", 10, {2: 40}),
            ("2", 0, {2: 250}),
            ("2", 10, {2: 240}),
            ("3", 0, {2: 250}),
            ("3", 10, {2: 240}),
            ("4", 0, {2: 350}),
            ("4", 10, {2: 340}),
        ],
    )
    def test_validate_sources(
        self, expected_result: dict[Literal[1, 2, 3], int], coffee_variant: str, coffee_value: int
    ) -> None:
        """Test validate sources"""
        self.TEST_CLASS.WATER_VALUE = coffee_value
        drink = self.TEST_CLASS.DRINKS[coffee_variant]
        test_result = self.TEST_CLASS.validate_sources(drink=drink)
        assert test_result == expected_result
