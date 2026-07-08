import unittest
from unittest.mock import MagicMock, patch
from services.package_service import PackageService
from enums.package_status import PackageStatus
from models.package import Package

class Initializer_Should(unittest.TestCase):
    def test_nothingBreaks(self):
        mock_app_data = MagicMock()
        PackageService(mock_app_data)
        

class CreatePackage_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.mock_app_data = MagicMock()
        self.package_service = PackageService(self.mock_app_data)

        # mock package class inside package_service
        patcher = patch("services.package_service.Package")
        self.mock_package_cls = patcher.start()
        # ran at end of setUp on each test
        self.addCleanup(patcher.stop)
        
        self.mock_app_data.generate_package_id.return_value = 1
        # get instance of the mocked class
        self.mock_package_instance = self.mock_package_cls.return_value
        
        # Act
        self.result = self.package_service.create_package("A", "B", 123, "email")

    def test_generateId_calledOnce(self):
        
        # Assert
        self.mock_app_data.generate_package_id.assert_called_once()
        
    def test_buildsPackageWithGeneratedId(self):

        # Assert
        self.mock_package_cls.assert_called_once_with(1,"A","B",123,"email")
    
    def test_addsPackage(self):
        
        # Assert
        self.mock_app_data.add_package.assert_called_once_with(self.mock_package_instance)
        
    def test_returnsCreatedPackage(self):

        # Assert
        self.assertEqual(self.result, self.mock_package_instance)
        
class GetPackageMethods_Should(unittest.TestCase):

    def setUp(self):
        
        # Arrange
        self.mock_app_data = MagicMock()
        self.package_service = PackageService(self.mock_app_data)
        
        self.mock_package1 = MagicMock(spec_set=Package)
        self.mock_package1.package_id = 1
        self.mock_package1.status = PackageStatus.IN_TRANSIT
        
        self.mock_package2 = MagicMock(spec_set=Package)
        self.mock_package2.package_id = 2
        self.mock_package2.status = PackageStatus.IN_TRANSIT
        
        self.mock_package3 = MagicMock(spec_set=Package)
        self.mock_package3.package_id = 3
        self.mock_package3.status = PackageStatus.NOT_ASSIGNED
        
        self.mock_packages = [self.mock_package1,
                              self.mock_package2,
                              self.mock_package3]
        self.mock_app_data.packages.values.return_value = self.mock_packages
        self.mock_app_data.find_package.return_value = "unrelated_to_the_test_data"
        
        
    def test_getPackage_findsPackage_withGivenId(self):

        # Act
        result = self.package_service.get_package(1)
        
        # Assert
        self.assertEqual(result, self.mock_app_data.find_package.return_value)
    
    def test_getPackage_callsFindPackageOnce_withCorrectId(self):
        
        # Act
        result = self.package_service.get_package(1)
        
        # Assert
        self.mock_app_data.find_package.assert_called_once_with(1)
        
    
    def test_getAllPackages_returnsCorrectPackages(self):
        
        # Act
        result = self.package_service.get_all_packages()

        # Assert
        self.assertEqual(result, self.mock_packages)
    
    def test_getAllPackages_returnsList(self):
        
        # Act
        result = self.package_service.get_all_packages()
    
        # Assert
        self.assertIsInstance(result, list)
    

    def test_getAllPackages_callsValuesOnce(self):
        
        # Act
        self.package_service.get_all_packages()
        
        # Assert
        self.mock_app_data.packages.values.assert_called_once()
        
    
        
    def test_getPackagesByStatus_returnsMatching(self):
        
        # Act
        result = self.package_service.get_packages_by_status(PackageStatus.IN_TRANSIT)
        
        # Assert
        # matching packages
        self.assertEqual(result, [self.mock_package1, self.mock_package2])
        # non-matching
        
    def test_getPackagesByStatus_notReturnsNonMatching(self):
        
        # Act
        result = self.package_service.get_packages_by_status(PackageStatus.IN_TRANSIT)
        
        # Assert
        self.assertNotIn(self.mock_package3, result)
    
    def test_getPackageByStatus_callsValuesOnce(self):

        # Act
        self.package_service.get_packages_by_status(PackageStatus.IN_TRANSIT)
        
        # Assert
        self.mock_app_data.packages.values.assert_called_once()
        

class MarkMethods_Should(unittest.TestCase):
    def setUp(self):
        self.mock_app_data = MagicMock()
        self.package_service = PackageService(self.mock_app_data)
        
        self.mock_package1 = MagicMock()
        self.mock_package1.status = PackageStatus.IN_TRANSIT
        
        patcher = patch.object(self.package_service, "get_package", return_value=self.mock_package1)
        self.mock_get_package = patcher.start()
        self.addCleanup(patcher.stop)

    def test_markInTransit_callsGetPackageOnce(self):
        
        # Act
        self.package_service.mark_in_transit(1)
        
        # Assert
        self.mock_get_package.assert_called_once_with(1)


    def test_markInTransit_changesStatus_whenValidData(self):
        
        # Act
        self.package_service.mark_in_transit(1)
        
        # Assert
        self.assertEqual(self.mock_package1.status, PackageStatus.IN_TRANSIT)
        
    def test_markInTransit_raiseError_whenStatusIsDelivered(self):
        # Arrange
        self.mock_package1.status = PackageStatus.DELIVERED
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.package_service.mark_in_transit(1)
    
    def test_markInTransit_doesNotChangeStatus_whenPackageIsDelivered(self):

        # Arrange
        self.mock_package1.status = PackageStatus.DELIVERED

        # Act, Assert
        with self.assertRaises(ValueError):
            self.package_service.mark_in_transit(1)
        self.assertEqual(self.mock_package1.status, PackageStatus.DELIVERED)
        
    def test_markDelivered_callsGetPackageOnce(self):
                
        # Act
        self.package_service.mark_delivered(1)
        
        # Assert
        self.mock_get_package.assert_called_once_with(1)
        
    def test_markDelivered_changesStatus_whenValidData(self):
        
        # Act
        self.package_service.mark_delivered(1)
        
        # Assert
        self.assertEqual(self.mock_package1.status, PackageStatus.DELIVERED)