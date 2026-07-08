import unittest
from unittest.mock import MagicMock
from core.application_data import ApplicationData
from enums.city import City

class ApplicationDataShould(unittest.TestCase):
    def setUp(self):
        self.app_data = ApplicationData()

    # ID Generation Tests

    def test_package_id_increases_each_time_it_is_called(self):
        # Act
        first_id = self.app_data.generate_package_id()
        second_id = self.app_data.generate_package_id()
        
        # Assert
        self.assertEqual(first_id, 1)
        self.assertEqual(second_id, 2)

    def test_route_id_increases_each_time_it_is_called(self):
        # Act
        first_id = self.app_data.generate_route_id()
        second_id = self.app_data.generate_route_id()
        
        # Assert
        self.assertEqual(first_id, 1)
        self.assertEqual(second_id, 2)

    def test_vehicle_id_increases_each_time_it_is_called(self):
        # Act
        first_id = self.app_data.generate_vehicle_id()
        second_id = self.app_data.generate_vehicle_id()
        
        # Assert
        self.assertEqual(first_id, 1)
        self.assertEqual(second_id, 2)

    # ID Sync/Observation Tests 

    def test_package_id_jumps_to_the_highest_observed_value(self):
        # Act
        self.app_data.observe_package_id(50)
        new_id = self.app_data.generate_package_id()
        
        # Assert
        self.assertEqual(new_id, 51)

    def test_route_id_jumps_to_the_highest_observed_value(self):
        # Act
        self.app_data.observe_route_id(50)
        new_id = self.app_data.generate_route_id()
        
        # Assert
        self.assertEqual(new_id, 51)

    def test_vehicle_id_jumps_to_the_highest_observed_value(self):
        # Act
        self.app_data.observe_vehicle_id(50)
        new_id = self.app_data.generate_vehicle_id()
        
        # Assert
        self.assertEqual(new_id, 51)

    # Saving
    def test_saving_a_package_makes_it_findable(self):
        # Arrange
        fake_package = MagicMock(package_id=10)
        
        # Act
        self.app_data.add_package(fake_package)
        
        # Assert
        self.assertIn(10, self.app_data.packages)

    def test_saving_a_route_makes_it_findable(self):
        # Arrange
        fake_route = MagicMock(route_id=10)
        
        # Act
        self.app_data.add_route(fake_route)
        
        # Assert
        self.assertIn(10, self.app_data.routes)

    def test_saving_a_vehicle_makes_it_findable(self):
        # Arrange
        fake_vehicle = MagicMock(vehicle_id=10)
        
        # Act
        self.app_data.add_vehicle(fake_vehicle)
        
        # Asser
        self.assertIn(10, self.app_data.vehicle_map)

    def test_saving_a_hub_by_city_makes_it_findable(self):
        # Arrange
        fake_hub = MagicMock(city=City.SYD)
        
        # Act
        self.app_data.add_hub(fake_hub)
        
        # Assert
        self.assertEqual(self.app_data.find_hub(City.SYD), fake_hub)

    # Finding Objects

    def test_finding_a_saved_package_returns_the_correct_object(self):
        # Arrange
        fake_package = MagicMock(package_id=1)
        self.app_data.add_package(fake_package)
        
        # Act
        found = self.app_data.find_package(1)
        
        # Assert
        self.assertEqual(found, fake_package)

    def test_finding_a_non_existent_package_gives_an_error(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            self.app_data.find_package(999)

    def test_finding_a_saved_route_returns_the_correct_object(self):
        # Arrange
        fake_route = MagicMock(route_id=1)
        self.app_data.add_route(fake_route)
        
        # Act
        found = self.app_data.find_route(1)
        
        # Assert
        self.assertEqual(found, fake_route)

    def test_finding_a_non_existent_route_gives_an_error(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            self.app_data.find_route(999)

    def test_finding_a_saved_vehicle_returns_the_correct_object(self):
        # Arrange
        fake_vehicle = MagicMock(vehicle_id=1)
        self.app_data.add_vehicle(fake_vehicle)
        
        # Act
        found = self.app_data.find_vehicle(1)
        
        # Assert
        self.assertEqual(found, fake_vehicle)

    def test_finding_a_non_existent_vehicle_gives_an_error(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            self.app_data.find_vehicle(999)

    def test_finding_a_saved_hub_returns_the_correct_object(self):
        # Arrange
        fake_hub = MagicMock(city=City.SYD)
        self.app_data.add_hub(fake_hub)
        
        # Act
        found = self.app_data.find_hub(City.SYD)
        
        # Assert
        self.assertEqual(found, fake_hub)

    def test_finding_a_hub_that_does_not_exist_gives_an_error(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            self.app_data.find_hub(City.MEL)