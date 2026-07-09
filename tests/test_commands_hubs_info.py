import unittest
from unittest.mock import MagicMock, patch
from commands.hubs_info_command import HubInfoCommand

class HubInfoCommandShould(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.mock_app_data = MagicMock()
        self.mock_hub_service = MagicMock()

    def test_init_raises_value_error_if_params_provided(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            HubInfoCommand(["invalid_param"], self.mock_app_data, self.mock_hub_service)

    def test_execute_calls_info_not_assigned_packages_by_city(self):
        # Arrange
        command = HubInfoCommand([], self.mock_app_data, self.mock_hub_service)
        expected_info = "Packages by city: SOF: 5, PLD: 3"
        self.mock_hub_service.info_not_assigned_packages_by_city.return_value = expected_info
        
        # Act
        result = command.execute()
        
        # Assert
        self.mock_hub_service.info_not_assigned_packages_by_city.assert_called_once()
        self.assertEqual(result, expected_info)