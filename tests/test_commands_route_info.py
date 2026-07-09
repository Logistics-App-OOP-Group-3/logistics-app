import unittest
from unittest.mock import MagicMock, patch
from commands.route_info_command import RouteInfoCommand

class RouteInfoCommandShould(unittest.TestCase):
    def setUp(self):
        self.mock_app_data = MagicMock()
        self.mock_route_service = MagicMock()
        self.params = ["101"]

    def test_init_raises_value_error_if_params_count_is_not_one(self):
        with self.assertRaises(ValueError):
            RouteInfoCommand([], self.mock_app_data, self.mock_route_service)

    @patch('commands.route_info_command.try_parse_int')
    def test_execute_returns_no_packages_message(self, mock_parse):
        # Arrange
        mock_parse.return_value = 101
        mock_route = MagicMock()
        mock_route.packages_ids = []
        mock_route.__str__.return_value = "Route 101 Details"
        self.mock_route_service.get_route.return_value = mock_route
        
        command = RouteInfoCommand(self.params, self.mock_app_data, self.mock_route_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertIn("No packages have been assigned", result)
        self.assertEqual(result, "Route 101 Details\nPackages: No packages have been assigned to this route.")

    @patch('commands.route_info_command.try_parse_int')
    def test_execute_returns_list_of_package_ids(self, mock_parse):
        # Arrange
        mock_parse.return_value = 101
        mock_route = MagicMock()
        mock_route.packages_ids = [1, 2, 3]
        mock_route.__str__.return_value = "Route 101 Details"
        self.mock_route_service.get_route.return_value = mock_route
        
        command = RouteInfoCommand(self.params, self.mock_app_data, self.mock_route_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertIn("Packages: 1, 2, 3", result)