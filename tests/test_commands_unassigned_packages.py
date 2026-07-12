import unittest
from unittest.mock import MagicMock
from commands.unassigned_packages_command import UnassignedPackagesCommand
from enums.package_status import PackageStatus

class UnassignedPackagesCommandShould(unittest.TestCase):
    def setUp(self):
        self.mock_app_data = MagicMock()
        self.mock_package_service = MagicMock()
        self.params = []

    def test_init_raises_value_error_if_params_provided(self):
        with self.assertRaises(ValueError):
            UnassignedPackagesCommand(["extra_param"], self.mock_app_data, self.mock_package_service)

    def test_execute_returns_message_if_no_packages_found(self):
        # Arrange
        self.mock_package_service.get_packages_by_status.return_value = []
        command = UnassignedPackagesCommand(self.params, self.mock_app_data, self.mock_package_service)
        
        # Act
        result = command.execute()
        
        # Assert
        self.assertEqual(result, "\nNo unassigned packages right now.\n")
        self.mock_package_service.get_packages_by_status.assert_called_once_with(PackageStatus.NOT_ASSIGNED)

    def test_execute_returns_newline_separated_package_info(self):
        # Arrange
        mock_pkg1 = MagicMock()
        mock_pkg1.short_info.return_value = "Package 1: Pending"
        mock_pkg2 = MagicMock()
        mock_pkg2.short_info.return_value = "Package 2: Ready"
        
        self.mock_package_service.get_packages_by_status.return_value = [mock_pkg1, mock_pkg2]
        command = UnassignedPackagesCommand(self.params, self.mock_app_data, self.mock_package_service)
        
        # Act
        result = command.execute()
        
        # Assert
        expected = "\nPackage 1: Pending\nPackage 2: Ready\n"
        self.assertEqual(result, expected)
        self.assertTrue(mock_pkg1.short_info.called)
        self.assertTrue(mock_pkg2.short_info.called)