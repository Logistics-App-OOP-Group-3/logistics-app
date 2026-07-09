import unittest
from unittest.mock import MagicMock
from commands.base.base_command import BaseCommand

# Creating a dummy command for testing purposes
class ConcreteCommand(BaseCommand):
    def execute(self) -> str:
        return "Executed"

class BaseCommandShould(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.mock_app_data = MagicMock()
        self.params = ["param1", "param2"]
        self.command = ConcreteCommand(self.params, self.mock_app_data)

    def test_params_are_stored_as_a_tuple(self):
        # Act and Assert
        self.assertIsInstance(self.command.params, tuple)
        self.assertEqual(self.command.params, ("param1", "param2"))

    def test_app_data_is_stored_correctly(self):
        # Act and Assert
        self.assertEqual(self.command.app_data, self.mock_app_data)

    def test_cannot_instantiate_base_command_directly(self):
        # Assert
        with self.assertRaises(TypeError):
            BaseCommand(["test"], self.mock_app_data)

    def test_subclass_must_implement_execute(self):
        # Act and assert
        self.assertEqual(self.command.execute(), "Executed")