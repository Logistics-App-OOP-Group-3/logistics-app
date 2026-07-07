import unittest
from unittest.mock import Mock
from models.hub import Hub
from enums.city import City
from enums.package_status import PackageStatus

VALID_CITY = City.MEL

class Initializer_Should(unittest.TestCase):
    
    def test_assignValues(self):
        # Arrange & Act
        hub = Hub(VALID_CITY)
        
        # Assert
        self.assertEqual(hub.city, VALID_CITY)
        self.assertEqual(hub.packages, tuple())
        self.assertEqual(hub.packages_ids, tuple())
        self.assertEqual(hub.delivered_packages, tuple())
        self.assertEqual(hub.delivered_packages_ids, tuple())        
        self.assertEqual(hub.packages_weight, 0)
        self.assertEqual(hub.package_count, 0)
        
class AddSinglePackage_Should(unittest.TestCase):
    
    def setUp(self):
        # Arrange
        self.hub = Hub(VALID_CITY)
        self.mock_package = Mock()
        self.mock_package.package_id = 1
        self.mock_package.weight = 50
        self.mock_package2 = Mock()
        self.mock_package2.package_id = 2
        self.mock_package2.weight = 50.50
    
    def test_withDefaultArg(self):
        # Act
        self.hub.add_single_package(self.mock_package)
        self.hub.add_single_package(self.mock_package2)

        # Assert
        self.assertEqual(self.hub.packages, tuple([self.mock_package, self.mock_package2]))
        self.assertEqual(self.hub.packages_ids, tuple([1,2]))
        self.assertEqual(self.hub.packages_weight, 100.50)
        self.assertEqual(self.hub.package_count, 2)
        
    def test_withExplicitArg(self):
        # Act
        self.hub.add_single_package(self.mock_package, delivered=True)
        self.hub.add_single_package(self.mock_package2, delivered=True)
        
        # Assert
        self.assertEqual(self.hub.delivered_packages, tuple([self.mock_package, self.mock_package2]))
        self.assertEqual(self.hub.delivered_packages_ids, tuple([1,2]))
        self.assertEqual(self.hub.packages_weight, 0)
        self.assertEqual(self.hub.package_count, 0)
          
    def test_withDefaultArg_raiseError_whenAlreadyAdded(self):
        
        # Act
        self.hub.add_single_package(self.mock_package)
        
        # Assert
        with self.assertRaises(ValueError):
            self.hub.add_single_package(self.mock_package)
            
    def test_withExplicitArg_raiseError_whenAlreadyAdded(self):
        
        # Act
        self.hub.add_single_package(self.mock_package, delivered=True)
        
        # Assert   
        with self.assertRaises(ValueError):
            self.hub.add_single_package(self.mock_package, delivered=True)
            
class RemoveSinglePackage_Should(unittest.TestCase):
    def setUp(self):
        
        # Arrange
        self.hub = Hub(VALID_CITY)
        self.mock_package = Mock()
        self.mock_package.package_id = 1
        self.mock_package.weight = 50
        self.mock_package2 = Mock()
        self.mock_package2.package_id = 2
        self.mock_package2.weight = 50.50
        self.hub.add_single_package(self.mock_package)
        self.hub.add_single_package(self.mock_package2)
        self.hub.add_single_package(self.mock_package, delivered = True)
        self.hub.add_single_package(self.mock_package2, delivered = True)

    def test_withDefaultArg(self):
        
        # Act
        self.hub.remove_single_package(self.mock_package.package_id)

        # Assert  
        self.assertEqual(self.hub.packages, tuple([self.mock_package2]))
        self.assertEqual(self.hub.packages_ids, tuple([2]))
        self.assertEqual(self.hub.packages_weight, 50.50)
        self.assertEqual(self.hub.package_count, 1)
        
    def test_withExplicitArg(self):
        
        # Act
        self.hub.remove_single_package(self.mock_package.package_id, from_delivered = True)

        # Assert
        self.assertEqual(self.hub.delivered_packages, tuple([self.mock_package2]))
        self.assertEqual(self.hub.delivered_packages_ids, tuple([2]))
        self.assertEqual(self.hub.packages_weight, 100.50)
        self.assertEqual(self.hub.package_count, 2)
        
    def test_withDefaultArg_raiseError_whenNotFound(self):
        
        # Act
        self.hub.remove_single_package(self.mock_package.package_id)
        
        # Assert
        with self.assertRaises(ValueError):
            self.hub.remove_single_package(self.mock_package.package_id)
            
    def test_withExplicitArg_raiseError_whenNotFound(self):
        
        # Act
        self.hub.remove_single_package(self.mock_package.package_id, from_delivered=True)
        
        # Assert   
        with self.assertRaises(ValueError):
            self.hub.remove_single_package(self.mock_package.package_id, from_delivered=True)

class Str_Should(unittest.TestCase):
    
    def test_returnsString(self):
        
        # Arrange
        hub = Hub(VALID_CITY)
        
        # Act
        result = str(hub).lower()
        
        # Assert
        self.assertIsInstance(result, str)
        self.assertIn(VALID_CITY.value.lower(), result)
        self.assertIn('package', result)
        self.assertIn('weight', result)

        
class info_not_assigned_packages_by_end_location_Should(unittest.TestCase):
    def setUp(self):
        
        # Arrange
        self.hub = Hub(VALID_CITY)
        self.mock_package = Mock()
        self.mock_package.package_id = 1
        self.mock_package.weight = 50
        self.mock_package.end_location = City.ADL
        self.mock_package.status = PackageStatus.NOT_ASSIGNED
        self.mock_package2 = Mock()
        self.mock_package2.package_id = 2
        self.mock_package2.weight = 50.50
        self.mock_package2.end_location = City.ADL
        self.mock_package2.status = PackageStatus.NOT_ASSIGNED
        self.hub.add_single_package(self.mock_package)
        self.hub.add_single_package(self.mock_package2)
        
    def test_groupsByEndLocation(self):

        # Act
        result = self.hub.info_not_assigned_packages_by_end_location()
        
        # Assert
        self.assertEqual(result.count(City.ADL.value), 1) 
    
    def test_countOnlyNotAssigned(self):
        
        # Arrange
        self.mock_package3 = Mock()
        self.mock_package3.package_id = 3
        self.mock_package3.weight = 50
        self.mock_package3.end_location = City.ADL
        self.mock_package3.status = PackageStatus.ASSIGNED
        self.hub.add_single_package(self.mock_package3)
        
        # Act
        result = self.hub.info_not_assigned_packages_by_end_location()
        lines = result.splitlines()
        adl_line = next(line for line in lines if f"{City.ADL.value}" in line)
        
        # Assert
        self.assertIn("2 package", adl_line)
    
    def test_sumsWeightPerLocation(self):
        
        # Arrange
        self.mock_package3 = Mock()
        self.mock_package3.package_id = 3
        self.mock_package3.weight = 75
        self.mock_package3.end_location = City.SYD
        self.mock_package3.status = PackageStatus.NOT_ASSIGNED
        self.hub.add_single_package(self.mock_package3)
        
        # Act
        result = self.hub.info_not_assigned_packages_by_end_location()
        lines = result.splitlines()
        adl_line = next(line for line in lines if f"{City.ADL.value}" in line)
        syd_line = next(line for line in lines if f"{City.SYD.value}" in line)
        
        # Assert
        self.assertIn("100.50", adl_line)
        self.assertIn("75.00", syd_line)

    def test_sortsInDescendingByWeight(self):
        
        # Arrange
        self.mock_package3 = Mock()
        self.mock_package3.package_id = 3
        self.mock_package3.weight = 150
        self.mock_package3.end_location = City.SYD
        self.mock_package3.status = PackageStatus.NOT_ASSIGNED
        self.hub.add_single_package(self.mock_package3)
        
        # Act
        result = self.hub.info_not_assigned_packages_by_end_location()
        lines = result.splitlines()
        adl_idx = next((i for i, line in enumerate(lines) if f"{City.ADL.value}" in line))
        syd_index = next((i for i, line in enumerate(lines) if f"{City.SYD.value}" in line))
        
        # Assert
        self.assertLess(syd_index, adl_idx)
        
        
class FindPackagesForLocations_Should(unittest.TestCase):
    def setUp(self):
        
        # Arrange
        self.hub = Hub(VALID_CITY)
        self.mock_package = Mock()
        self.mock_package.package_id = 1
        self.mock_package.weight = 50
        self.mock_package.end_location = City.ADL
        self.mock_package.route_id = 1
        self.mock_package2 = Mock()
        self.mock_package2.package_id = 2
        self.mock_package2.weight = 50.50
        self.mock_package2.end_location = City.ADL
        self.mock_package2.route_id = None
        self.hub.add_single_package(self.mock_package)
        self.hub.add_single_package(self.mock_package2)
        
    def test_filterOnlyNotAssigned(self):
        
        # Act
        result = self.hub.find_packages_for_locations([City.ADL, City.ASP])

        # Assert
        self.assertEqual(result, [self.mock_package2])
        
    def test_findForDifferentEndlocations(self):
        
        # Arrange
        self.mock_package3 = Mock()
        self.mock_package3.package_id = 3
        self.mock_package3.weight = 50
        self.mock_package3.end_location = City.ASP
        self.mock_package3.route_id = None
        self.hub.add_single_package(self.mock_package3)
        
        # Act
        result = self.hub.find_packages_for_locations([City.ADL, City.ASP])

        # Assert
        self.assertEqual(result, [self.mock_package2, self.mock_package3])
        