import unittest
from unittest.mock import MagicMock, patch
from commands.package_info_command import PackageInfoCommand

class PackageInfoCommandShould(unittest.TestCase):
    def setUp(self):
        self.mock_app_data = MagicMock()
        self.mock_package_service = MagicMock()
        self.mock_route_service = MagicMock()
        self.params = ["123"]

    def test_init_raises_value_error_if_params_count_is_not_one(self):
        with self.assertRaises(ValueError):
            PackageInfoCommand([], self.mock_app_data, self.mock_package_service, self.mock_route_service)

    @patch('commands.package_info_command.try_parse_int')
    def test_execute_returns_package_info_without_eta_if_no_route(self, mock_parse):
        # Arrange
        mock_parse.return_value = 123
        mock_package = MagicMock()
        mock_package.route_id = None
        mock_package.__str__.return_value = "Package 123 details"
        self.mock_package_service.get_package.return_value = mock_package
        
        command = PackageInfoCommand(self.params, self.mock_app_data, 
                                     self.mock_package_service, self.mock_route_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertEqual(result, "\nPackage 123 details\n")
        self.mock_route_service.get_eta_for_location.assert_not_called()

    @patch('commands.package_info_command.try_parse_int')
    def test_execute_returns_package_info_with_eta_if_on_route(self, mock_parse):
        # Arrange
        mock_parse.return_value = 123
        mock_package = MagicMock()
        mock_package.route_id = 1
        mock_package.end_location = "SOF"
        mock_package.__str__.return_value = "Package 123 details"
        self.mock_package_service.get_package.return_value = mock_package
        
        from datetime import datetime
        self.mock_route_service.get_eta_for_location.return_value = datetime(2026, 7, 20, 14, 30)
        
        command = PackageInfoCommand(self.params, self.mock_app_data, 
                                     self.mock_package_service, self.mock_route_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertIn("Package 123 details", result)
        self.assertIn("Expected arrival time: 20/07/2026 14:30", result)
        self.mock_route_service.get_eta_for_location.assert_called_once()