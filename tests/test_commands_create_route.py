import unittest
from unittest.mock import MagicMock, patch
from commands.create_route_command import CreateRouteCommand

class CreateRouteCommandShould(unittest.TestCase):
    def setUp(self):
        self.mock_app_data = MagicMock()
        self.mock_route_service = MagicMock()
        self.mock_vehicle_service = MagicMock()
        self.params = ["SOF", "PLD", "VAR"]

    @patch('commands.create_route_command.vh')
    def test_execute_raises_value_error_if_no_vehicle_available(self, mock_vh):
        # Arrange: Setup mock helper
        mock_vh.try_parse_city.side_effect = lambda x: x 
        
        mock_route = MagicMock()
        mock_route.total_distance = 500
        self.mock_route_service.create_route.return_value = mock_route
        self.mock_vehicle_service.find_available_vehicle_for_distance.return_value = None

        # Act and Assert
        command = CreateRouteCommand(self.params, self.mock_app_data, 
                                     self.mock_route_service, self.mock_vehicle_service)
        with self.assertRaises(ValueError) as cm:
            command.execute()
        
        self.assertIn("No vehicle available", str(cm.exception))

    @patch('commands.create_route_command.vh')
    def test_execute_starts_route_when_vehicle_is_available(self, mock_vh):
        # Arrange: Setup mock helper
        mock_vh.try_parse_city.side_effect = lambda x: x 
        
        mock_route = MagicMock()
        mock_route.total_distance = 500
        mock_route.__str__.return_value = "Route Info"
        self.mock_route_service.create_route.return_value = mock_route
        
        mock_vehicle = MagicMock()
        self.mock_vehicle_service.find_available_vehicle_for_distance.return_value = mock_vehicle

        # Act
        command = CreateRouteCommand(self.params, self.mock_app_data, 
                                     self.mock_route_service, self.mock_vehicle_service)
        result = command.execute()

        # Assert
        self.mock_route_service.assign_truck_to_route.assert_called_once_with(mock_route, mock_vehicle)
        self.mock_route_service.assign_packages_from_hubs.assert_called_once_with(mock_route, mock_vehicle)
        self.mock_route_service.start_route.assert_called_once_with(mock_route)
        self.assertIn("Route created successfully", result)