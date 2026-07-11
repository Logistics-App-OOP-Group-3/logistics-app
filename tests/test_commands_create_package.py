import unittest
from unittest.mock import MagicMock, patch
from commands.create_package_command import CreatePackageCommand

class CreatePackageCommandShould(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.mock_app_data = MagicMock()
        self.mock_package_service = MagicMock()
        self.mock_route_service = MagicMock()  # Added dependency
        self.params = ["MEL", "PLD", "10.5", "0888123456"]

    def test_init_raises_value_error_if_params_count_is_not_four(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            CreatePackageCommand(["MEL", "PLD"], self.mock_app_data, 
                                 self.mock_package_service, self.mock_route_service)

    @patch('commands.create_package_command.val_help')
    def test_execute_creates_package_and_displays_no_routes_found(self, mock_val_help):
        # Arrange
        command = CreatePackageCommand(self.params, self.mock_app_data, 
                                       self.mock_package_service, self.mock_route_service)
        
        mock_val_help.try_parse_city.side_effect = lambda x: x
        mock_val_help.try_parse_float.return_value = 10.5
        
        mock_package = MagicMock()
        mock_package.package_id = 99
        self.mock_package_service.create_package.return_value = mock_package
        
        mock_hub = MagicMock()
        mock_hub.city.value = "MEL"
        self.mock_app_data.find_hub.return_value = mock_hub
        
        # Mock finding no routes
        self.mock_route_service.find_routes_for_package.return_value = []
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertIn("Package 99 created successfully", result)
        self.assertIn("No available routes currently found", result)

    @patch('commands.create_package_command.val_help')
    def test_execute_creates_package_and_displays_available_routes(self, mock_val_help):
        # Arrange
        command = CreatePackageCommand(self.params, self.mock_app_data, 
                                       self.mock_package_service, self.mock_route_service)
        
        mock_val_help.try_parse_city.side_effect = lambda x: x
        mock_val_help.try_parse_float.return_value = 10.5
        
        mock_package = MagicMock()
        mock_package.package_id = 99
        self.mock_package_service.create_package.return_value = mock_package
        
        mock_hub = MagicMock()
        mock_hub.city.value = "MEL"
        self.mock_app_data.find_hub.return_value = mock_hub
        
        # Mock finding a route
        mock_route = MagicMock()
        mock_route.route_id = 1
        mock_route.route_stops_info.return_value = "Stop Info Details"
        self.mock_route_service.find_routes_for_package.return_value = [mock_route]
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertIn("Route #1", result)
        self.assertIn("Stop Info Details", result)
        self.mock_route_service.find_routes_for_package.assert_called_once_with(mock_package)