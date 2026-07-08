import unittest
from unittest.mock import MagicMock, patch
from services.vehicle_service import VehicleService
from models.vehicle import Vehicle


class Initializer_Should(unittest.TestCase):

    def test_nothingBreaks(self):
        mock_app_data = MagicMock()
        VehicleService(mock_app_data)
        
    
class GetMethods_Shoud(unittest.TestCase):
    def setUp(self):
    
        # Arrange
        self.mock_app_data = MagicMock()
        self.vehicle_service = VehicleService(self.mock_app_data)
        self.mock_app_data.find_vehicle.return_value = "unrelated_to_the_test_data"

        self.mock_vehicles = [MagicMock(), MagicMock()]
        self.mock_app_data.vehicles = self.mock_vehicles
        
    def test_getVehicle_findsVehicle_withGivenId(self):
        
        # Act
        result = self.vehicle_service.get_vehicle(1)
        
        # Assert
        self.mock_app_data.find_vehicle.assert_called_once_with(1)
        self.assertEqual(result, self.mock_app_data.find_vehicle.return_value)

    def test_getAllVehicles_returnsCorrectVehicles(self):
        
        # Act
        result = self.vehicle_service.get_all_vehicles()
        
        # Assert
        self.assertEqual(result, self.mock_vehicles)
        
    def test_getAllVehicles_returnsList(self):
                
        # Act
        result = self.vehicle_service.get_all_vehicles()
        
        # Assert
        self.assertIsInstance(result, list)


class FindAvailableVehicleForDistance_Should(unittest.TestCase):
    def setUp(self):
    
        # Arrange
        self.mock_app_data = MagicMock()
        self.vehicle_service = VehicleService(self.mock_app_data)

        self.mock_vehicles = [
            MagicMock(spec_set = Vehicle, route_id = 1, max_range = 500),
            MagicMock(spec_set = Vehicle, route_id = None, max_range = 500),
            MagicMock(spec_set = Vehicle, route_id = None, max_range = 1000),
            MagicMock(spec_set = Vehicle, route_id = None, max_range = 1000)
            
            ]
        self.mock_app_data.vehicles = self.mock_vehicles
        
    def test_returnsFirstVehicle_withRouteIdNone_whenDistanceMatchAll(self):
        
        # Act
        result = self.vehicle_service.find_available_vehicle_for_distance(100)
        
        # Assert
        self.assertEqual(result, self.mock_vehicles[1])
        
    def test_skipsNotMatchingDistances_returnsFirstVehicle_withRouteIdNone(self):
        
        # Act
        result = self.vehicle_service.find_available_vehicle_for_distance(600)

        # Assert
        self.assertEqual(result, self.mock_vehicles[2])
        
    def test_returnsNone_whenAllVehiclesRouteIdIsNotNone(self):
        
        # Arrange
        self.mock_vehicles[1].route_id = 2
        self.mock_vehicles[2].route_id = 3
        self.mock_vehicles[3].route_id = 4
        
        
        # Act
        result = self.vehicle_service.find_available_vehicle_for_distance(100)
        
        # Assert
        self.assertIsNone(result)    
        
    def test_returnsNone_whenDistanceIsBiggerThanAllVehiclesMaxRange(self):    
    
        # Act
        result = self.vehicle_service.find_available_vehicle_for_distance(2000)

        # Assert
        self.assertIsNone(result)  