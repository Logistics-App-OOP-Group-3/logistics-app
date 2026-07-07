import unittest
from unittest.mock import MagicMock
from services.hub_service import HubService
from enums.package_status import PackageStatus
from enums.city import City


class TestHubService(unittest.TestCase):
    def setUp(self):
        self.mock_data = MagicMock()

        self.hub_syd = MagicMock()
        self.hub_syd.city = City.SYD

        package0 = MagicMock(weight=200, status=PackageStatus.NOT_ASSIGNED)
        package1 = MagicMock(weight=100, status=PackageStatus.ASSIGNED)
        self.hub_syd.packages = [package0, package1]

        self.hub_mel = MagicMock()
        self.hub_mel.city = City.MEL

        package2 = MagicMock(weight=200, status=PackageStatus.NOT_ASSIGNED)
        self.hub_mel.packages = [package2]

        self.mock_data.hubs = [self.hub_syd, self.hub_mel]
        
        self.service = HubService(self.mock_data)
    
    def test_total_not_assigned_weight_by_city(self):
        result = self.service._total_not_assigned_weight_by_city()

        self.assertIn(City.MEL, result)
        self.assertIn(City.SYD, result)
        
        self.assertEqual(result[City.MEL], (200, 1))
        self.assertEqual(result[City.SYD], (200, 1))

    def test_info_not_assigned_packages_by_city(self):
        output = self.service.info_not_assigned_packages_by_city()

        self.assertIn("Sydney", output) 
        self.assertIn("Melbourne", output)
        self.assertIn("200.00", output)
        self.assertIn("1 package", output)
        self.assertIn("HUB", output)