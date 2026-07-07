import unittest
from unittest.mock import MagicMock, patch
from models.vehicle import Vehicle

VALID_ID = 1001
VALID_NAME = "Actros"
VALID_CAPACITY = 25000
VALID_MAX_RANGE = 13000

VEHICLE = Vehicle(VALID_ID, VALID_NAME, VALID_CAPACITY, VALID_MAX_RANGE)
VEHICLE.route_id = 1

class Initializer_Should(unittest.TestCase):
    
    def test_assignValues(self):

        # Assert
        self.assertEqual(VEHICLE.vehicle_id, VALID_ID)
        self.assertEqual(VEHICLE.name, VALID_NAME)
        self.assertEqual(VEHICLE.max_capacity, VALID_CAPACITY)
        self.assertEqual(VEHICLE.max_range, VALID_MAX_RANGE)
        self.assertEqual(VEHICLE.route_id, 1)
    
class ToCsv_Should(unittest.TestCase):

    def test_exportCorrectValues(self):
        # Act
        csv_line = VEHICLE.to_csv()
        
        # Assert
        self.assertIsInstance(csv_line, str)
        self.assertIn(str(VALID_ID), csv_line)
        self.assertIn(VALID_NAME, csv_line)
        self.assertIn(str(VALID_CAPACITY), csv_line)
        self.assertIn(str(VALID_MAX_RANGE), csv_line)
        
class Str_Should(unittest.TestCase):
    
    def test_returnTypeAndAttributesIncluded(self):
        
        # Act
        result = str(VEHICLE)

        # Assert
        self.assertIsInstance(result, str)
        self.assertIn(str(VALID_ID), result)
        self.assertIn(VALID_NAME, result)
        self.assertIn(str(VALID_CAPACITY), result)
        self.assertIn(str(VALID_MAX_RANGE), result)
        




