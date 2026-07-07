import unittest
from unittest.mock import MagicMock
from services.hub_service import HubService
from enums.package_status import PackageStatus
from enums.city import City

class HubService_Should(unittest.TestCase):

    def setUp(self):
        self.mock_data = MagicMock()
        self.service = HubService(self.mock_data)

    def test_total_not_assigned_weight_by_city_ReturnsSortedDescending(self):
        # Create two hubs with different weights to test sorting
        hub_low_weight = MagicMock(city=City.SYD, packages=[MagicMock(weight=100, status=PackageStatus.NOT_ASSIGNED)])
        hub_high_weight = MagicMock(city=City.MEL, packages=[MagicMock(weight=300, status=PackageStatus.NOT_ASSIGNED)])
        self.mock_data.hubs = [hub_low_weight, hub_high_weight]

        result = self.service._total_not_assigned_weight_by_city()

        self.assertEqual(list(result.keys())[0], City.MEL) # Higher weight first
        self.assertEqual(result[City.MEL], (300, 1))
        self.assertEqual(result[City.SYD], (100, 1))

    def test_total_not_assigned_weight_by_city_ReturnsZero_WhenNoNotAssignedPackages(self):
        # Hub with only assigned packages
        hub = MagicMock(city=City.BRI, packages=[MagicMock(weight=500, status=PackageStatus.ASSIGNED)])
        self.mock_data.hubs = [hub]

        result = self.service._total_not_assigned_weight_by_city()

        self.assertEqual(result[City.BRI], (0, 0))

    def test_total_not_assigned_weight_by_city_ReturnsZero_WhenHubIsEmpty(self):
        # Hub with no packages 
        hub = MagicMock(city=City.ADL, packages=[])
        self.mock_data.hubs = [hub]

        result = self.service._total_not_assigned_weight_by_city()

        self.assertEqual(result[City.ADL], (0, 0))

    def test_info_not_assigned_packages_by_city_FormatsCorrectly_ForPlural(self):
        hub = MagicMock(city=City.SYD, packages=[
            MagicMock(weight=10, status=PackageStatus.NOT_ASSIGNED),
            MagicMock(weight=20, status=PackageStatus.NOT_ASSIGNED)
        ])
        self.mock_data.hubs = [hub]

        output = self.service.info_not_assigned_packages_by_city()

        self.assertIn("30.00", output)
        self.assertIn("2 packages", output)

    def test_info_not_assigned_packages_by_city_FormatsCorrectly_ForSingular(self):
        hub = MagicMock(city=City.SYD, packages=[
            MagicMock(weight=10, status=PackageStatus.NOT_ASSIGNED)
        ])
        self.mock_data.hubs = [hub]

        output = self.service.info_not_assigned_packages_by_city()

        self.assertIn("10.00", output)
        self.assertIn("1 package", output)

    def test_info_not_assigned_packages_by_city_ContainsHeaders(self):
        self.mock_data.hubs = []

        output = self.service.info_not_assigned_packages_by_city()

        self.assertIn("HUB", output)
        self.assertIn("WEIGHT", output)
        self.assertIn("COUNT", output)