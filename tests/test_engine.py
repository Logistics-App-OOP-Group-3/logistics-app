import unittest
from unittest.mock import MagicMock, patch
from core.engine import Engine

class EngineShould(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.mock_factory = MagicMock()
        self.engine = Engine(self.mock_factory)

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    def test_engine_executes_valid_command(self, mock_print, mock_input):
        # Arrange
        mock_input.side_effect = ["ValidCommand", "exit"]
        
        # Create a mock command 
        mock_command = MagicMock()
        mock_command.execute.return_value = "Success"
        self.mock_factory.create.return_value = mock_command

        # Act
        self.engine.start()

        # Assert
        mock_command.execute.assert_called_once()
        mock_print.assert_called_with("Success")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    def test_engine_prints_error_message_on_value_error(self, mock_os, mock_print, mock_input):
        # Arrange
        mock_input.side_effect = ["BadCommand", "exit"]
        self.mock_factory.create.side_effect = ValueError("Invalid command!")

        # Act
        self.engine.start()

        # Assert
        mock_print.assert_called_with("Invalid command!")

    @patch('builtins.input')
    @patch('os.system')
    def test_engine_saves_data_when_user_exits(self, mock_os, mock_input):
        # Arrange
        mock_input.return_value = "exit"

        # Act
        self.engine.start()

        # Assert
        self.mock_factory._data_repository.save.assert_called_once()

    @patch('builtins.input')
    @patch('os.system')
    def test_engine_clears_the_console_on_startup(self, mock_os, mock_input):
        # Arrange
        mock_input.return_value = "exit"

        # Act
        self.engine.start()

        # Assert
        mock_os.assert_called()