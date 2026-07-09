import unittest
from unittest.mock import MagicMock, patch
from commands.create_package_command import CreatePackageCommand

class CreatePackageCommandShould(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.mock_app_data = MagicMock()
        self.mock_package_service = MagicMock()
        self.params = ["SOF", "PLD", "10.5", "0888123456"]

    def test_init_raises_value_error_if_params_count_is_not_four(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            CreatePackageCommand(["SOF", "PLD"], self.mock_app_data, self.mock_package_service)

    @patch('commands.create_package_command.val_help')
    def test_execute_creates_package_and_adds_to_hub(self, mock_val_help):
        # Arrange: Setup the commanod
        command = CreatePackageCommand(self.params, self.mock_app_data, self.mock_package_service)
        
        # Configure the mock helper to bypass real enum parsing
        mock_val_help.try_parse_city.side_effect = lambda x: x  # Return the input string
        mock_val_help.try_parse_float.return_value = 10.5
        
        # Setup mock package
        mock_package = MagicMock()
        mock_package.package_id = 99
        self.mock_package_service.create_package.return_value = mock_package
        
        # Setup mock hub
        mock_hub = MagicMock()
        mock_hub.city.value = "SOF"
        self.mock_app_data.find_hub.return_value = mock_hub
        
        # Act
        result = command.execute()
        
        # Assert
        self.mock_package_service.create_package.assert_called_once_with("SOF", "PLD", 10.5, "0888123456")
        self.mock_app_data.find_hub.assert_called_with("SOF")
        mock_hub.add_single_package.assert_called_with(mock_package)

        self.assertIn("Package 99 created successfully", result)