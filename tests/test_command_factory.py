import unittest
from unittest.mock import MagicMock, patch
from core.command_factory import CommandFactory
from commands.create_package_command import CreatePackageCommand
from commands.assign_package_command import AssignPackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.unassigned_packages_command import UnassignedPackagesCommand
from commands.hubs_info_command import HubInfoCommand
from commands.inspect_hub_command import InspectHubCommand
from commands.package_info_command import PackageInfoCommand
from commands.route_info_command import RouteInfoCommand
from commands.advance_routes_command import AdvanceRoutesCommand
from commands.routes_in_progress_info_command import RoutesInProgressInfoCommand

class CommandFactoryShould(unittest.TestCase):
    def setUp(self):
        # Arrange mock appdata
        self.mock_app_data = MagicMock()
        
        # patch the dependencies
        with patch('core.data_repository.DataRepository'):
            self.factory = CommandFactory(self.mock_app_data)

    def test_create_package_command_is_returned_for_create_package(self):
        # Act
        command = self.factory.create("CreatePackage 1 2 3 4")
        # Assert
        self.assertIsInstance(command, CreatePackageCommand)

    def test_assign_package_command_is_returned_for_assign_package(self):
        # Act
        command = self.factory.create("AssignPackage 1 1")
        # Assert
        self.assertIsInstance(command, AssignPackageCommand)

    def test_create_route_command_is_returned_for_create_route(self):
        # Act
        command = self.factory.create("CreateRoute 1 2")
        # Assert
        self.assertIsInstance(command, CreateRouteCommand)

    def test_unassigned_packages_command_is_returned(self):
        # Act
        command = self.factory.create("UnassignedPackages")
        # Assert
        self.assertIsInstance(command, UnassignedPackagesCommand)

    def test_hubs_info_command_is_returned(self):
        # Act
        command = self.factory.create("HubsInfo")
        # Assert
        self.assertIsInstance(command, HubInfoCommand)

    def test_inspect_hub_command_is_returned(self):
        # Act
        command = self.factory.create("InspectHub SYD")
        # Assert
        self.assertIsInstance(command, InspectHubCommand)

    def test_package_info_command_is_returned(self):
        # Act
        command = self.factory.create("PackageInfo 1")
        # Assert
        self.assertIsInstance(command, PackageInfoCommand)

    def test_route_info_command_is_returned(self):
        # Act
        command = self.factory.create("RouteInfo 1")
        # Assert
        self.assertIsInstance(command, RouteInfoCommand)

    def test_advance_routes_command_is_returned(self):
        # Act
        command = self.factory.create("AdvanceRoutes")
        # Assert
        self.assertIsInstance(command, AdvanceRoutesCommand)

    def test_routes_in_progress_command_is_returned(self):
        # Act
        command = self.factory.create("RoutesInProgress")
        # Assert
        self.assertIsInstance(command, RoutesInProgressInfoCommand)

    def test_factory_raises_error_for_unknown_command(self):
        # Act and assert
        with self.assertRaises(ValueError):
            self.factory.create("UnknownCommand 123")