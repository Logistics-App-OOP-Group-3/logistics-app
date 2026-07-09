import unittest
from unittest.mock import MagicMock
from commands.assign_package_command import AssignPackageCommand

class AssignPackageCommandShould(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.mock_app_data = MagicMock()
        self.mock_route_service = MagicMock()
        self.package_id = "1"
        self.route_id = "2"

    def test_init_raises_value_error_if_params_are_not_two(self):
        # Act and Assert expects 2 parameters
        with self.assertRaises(ValueError):
            AssignPackageCommand(["1"], self.mock_app_data, self.mock_route_service)

    def test_execute_returns_hub_message_if_route_id_is_zero(self):
        # Arrange
        params = ["1", "0"]
        command = AssignPackageCommand(params, self.mock_app_data, self.mock_route_service)
        
        mock_package = MagicMock()
        mock_package.start_location.value = "SYD"
        self.mock_app_data.find_package.return_value = mock_package
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertIn("remains at hub SYD", result)
        self.mock_route_service.assign_package_to_route.assert_not_called()

    def test_execute_calls_service_when_route_id_is_valid(self):
        # Arrange
        params = [self.package_id, self.route_id]
        command = AssignPackageCommand(params, self.mock_app_data, self.mock_route_service)
        
        mock_package = MagicMock()
        self.mock_app_data.find_package.return_value = mock_package
        
        # Act
        result = command.execute()
        
        # Assert
        self.mock_route_service.assign_package_to_route.assert_called_once_with(mock_package, 2)
        self.assertIn("assigned to route 2 successfully", result)