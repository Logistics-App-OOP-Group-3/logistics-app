import unittest
from unittest.mock import MagicMock
from commands.advance_routes_command import AdvanceRoutesCommand

class AdvanceRoutesCommandShould(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.mock_app_data = MagicMock()
        self.mock_route_service = MagicMock()

    def test_init_raises_value_error_if_params_provided(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            AdvanceRoutesCommand(["unexpected_param"], self.mock_app_data, self.mock_route_service)

    def test_execute_calls_complete_all_routes_next_stop_on_service(self):
        # Arrange
        command = AdvanceRoutesCommand([], self.mock_app_data, self.mock_route_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.mock_route_service.complete_all_routes_next_stop.assert_called_once()
        # Verify the output message
        self.assertEqual(result, "All routes advanced to their next stop.\n")