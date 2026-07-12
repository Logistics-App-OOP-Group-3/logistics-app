import unittest
from unittest.mock import MagicMock
from commands.routes_in_progress_info_command import RoutesInProgressInfoCommand
from enums.route_status import RouteStatus

class RoutesInProgressInfoCommandShould(unittest.TestCase):
    def setUp(self):
        self.mock_app_data = MagicMock()
        self.mock_route_service = MagicMock()
        self.params = []

    def test_execute_returns_no_routes_message_if_empty(self):
        # Arrange
        self.mock_route_service.get_routes_by_status.return_value = []
        command = RoutesInProgressInfoCommand(self.params, self.mock_app_data, self.mock_route_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertEqual(result, "\nNo routes are currently in progress.\n")
        self.mock_route_service.get_routes_by_status.assert_called_once_with(RouteStatus.IN_PROGRESS)

    def test_execute_returns_formatted_list_of_routes(self):
        # Arrange
        mock_route = MagicMock()
        mock_route.__str__.return_value = "Route ID: 1, Destination: SOF"
        self.mock_route_service.get_routes_by_status.return_value = [mock_route]
        
        command = RoutesInProgressInfoCommand(self.params, self.mock_app_data, self.mock_route_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertIn("--- Routes In Progress ---", result)
        self.assertIn("Route ID: 1, Destination: SOF", result)
        self.assertIn("-" * 30, result)