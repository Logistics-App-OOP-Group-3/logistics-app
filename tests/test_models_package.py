import unittest
from models.package import Package
from enums.package_status import PackageStatus
from enums.city import City

VALID_PACKAGE_ID = 1
VALID_START_LOCATION = City.MEL
VALID_END_LOCATION = City.ADL
VALID_WEIGHT = 40.50
VALID_CONTACT_INFO = "pesho@gmail.com"
VALID_ROUTE_ID = 1
VALID_STATUS = PackageStatus.ASSIGNED
DEFAULT_STATUS = PackageStatus.NOT_ASSIGNED
DEFAULT_ROUTE_ID = None

class Initializer_Should(unittest.TestCase):
    
    def test_assignValues(self):
        
        # Arrange, Act
        package = Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            VALID_WEIGHT,
            VALID_CONTACT_INFO
            )
        
        # Assert
        self.assertEqual(package.package_id, VALID_PACKAGE_ID)
        self.assertEqual(package.start_location, VALID_START_LOCATION)
        self.assertEqual(package.end_location, VALID_END_LOCATION)
        self.assertEqual(package.current_location, VALID_START_LOCATION)
        self.assertEqual(package.weight, VALID_WEIGHT)
        self.assertEqual(package.contact_info, VALID_CONTACT_INFO)
        self.assertEqual(package.status, DEFAULT_STATUS)
        self.assertEqual(package.route_id, DEFAULT_ROUTE_ID)
        
    def test_raiseError_whenInvalidEndLocation(self):

        # Arrange, Act, Assert
        with self.assertRaises(ValueError):
            Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_START_LOCATION,
            VALID_WEIGHT,
            VALID_CONTACT_INFO
            )
            
    def test_raiseError_whenWeightZero(self):

        # Arrange, Act, Assert
        with self.assertRaises(ValueError):
            Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            0,
            VALID_CONTACT_INFO
            )
    
    def test_raiseError_whenWeightTooHigh(self):

        # Arrange, Act, Assert
        with self.assertRaises(ValueError):
            Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            100000,
            VALID_CONTACT_INFO
            )
    
    def test_raiseError_whenContactInfoEmptyString(self):

        # Arrange, Act, Assert
        with self.assertRaises(ValueError):
            Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            VALID_WEIGHT,
            ""
            )
            
    def test_raiseError_whenContactInfoTooLong(self):
        
        # Arrange, Act, Assert
        with self.assertRaises(ValueError):
            Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            VALID_WEIGHT,
            "*" * 1000
            )
            
    def test_whenSettingStatus(self):
         # Arrange
        package = Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            VALID_WEIGHT,
            VALID_CONTACT_INFO
            )
        
        # Act
        package.status = VALID_STATUS
        
        # Assert
        self.assertEqual(package.status, VALID_STATUS)
            

            
class AssignToRouteShould(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.package = Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            VALID_WEIGHT,
            VALID_CONTACT_INFO
            )
    
    def test_assignsRouteID(self):
        
        # Act
        self.package.assign_to_route(1)
        
        # Assert
        self.assertEqual(self.package.route_id, 1)
    
    def test_assignsStatusAsAssigned(self):
        
        # Act
        self.package.assign_to_route(1)
        
        # Assert
        self.assertEqual(self.package.status, PackageStatus.ASSIGNED)
        
    def test_raiseError_whenSettingRouteIdNone(self):
    
        # Act, Assert
        with self.assertRaises(ValueError):
            self.package.assign_to_route(None)
        
class DeliveryMethods_Should(unittest.TestCase):
    def setUp(self):
        
        # Arrange
        self.package = Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            VALID_WEIGHT,
            VALID_CONTACT_INFO
            )
    
    def test_StartDeliveryAssignsStatusAsInTransit(self):
        
        # Act
        self.package.start_delivery()

        # Assert
        self.assertEqual(self.package.status, PackageStatus.IN_TRANSIT)

    def test_MarkDeliveredAssignsStatusAsDelivered(self):
        
        # Act
        self.package.mark_delivered()

        # Assert
        self.assertEqual(self.package.status, PackageStatus.DELIVERED)
        
class StrMethods_Should(unittest.TestCase):
    def setUp(self):
        
        # Arrange
        self.package = Package(
            VALID_PACKAGE_ID,
            VALID_START_LOCATION,
            VALID_END_LOCATION,
            VALID_WEIGHT,
            VALID_CONTACT_INFO
        )
    
    def test_strDunder(self):
        
        # Act
        result = str(self.package)
        
        # Assert
        self.assertIsInstance(result, str)
        self.assertIn(str(VALID_PACKAGE_ID), result)
        self.assertIn(VALID_START_LOCATION.value, result)
        self.assertIn(VALID_END_LOCATION.value, result)
        self.assertIn(DEFAULT_STATUS.value, result)
        self.assertIn(str(VALID_WEIGHT), result)
        self.assertIn(VALID_CONTACT_INFO, result)
        self.assertIn("Current", result)
        
    def test_ShortInfo(self):
        
        # Act
        result = self.package.short_info()

        # Assert
        self.assertIsInstance(result, str)
        self.assertIn(str(VALID_PACKAGE_ID), result)
        self.assertIn(VALID_START_LOCATION.value, result)
        self.assertIn(VALID_END_LOCATION.value, result)
        






        
    