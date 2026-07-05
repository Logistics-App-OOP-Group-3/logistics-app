from __future__ import annotations

from typing import TYPE_CHECKING

from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.package_info_command import PackageInfoCommand
from commands.route_info_command import RouteInfoCommand
from commands.unassigned_packages_command import UnassignedPackagesCommand
from commands.hubs_info_command import HubInfoCommand
from commands.inspect_hub_command import InspectHubCommand
from commands.advance_routes_command import AdvanceRoutesCommand
from services.route_service import RouteService
from services.package_service import PackageService
from services.vehicle_service import VehicleService
from services.hub_service import HubService
from core.data_repository import DataRepository

if TYPE_CHECKING:
    from core.application_data import ApplicationData


class CommandFactory:
    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data

        # services
        self._route_service = RouteService(app_data)
        self._package_service = PackageService(app_data)
        self._vehicle_service = VehicleService(app_data)
        self._hub_service = HubService(app_data)

        self._data_repository = DataRepository(app_data)
        self._data_repository.load()

    def create(self, input_line: str):
        cmd, *params = input_line.split()
        cmd = cmd.lower()

        if cmd == "createpackage":
            return CreatePackageCommand(
                params,
                self._app_data,
                self._package_service,
                self._route_service
            )

        if cmd == "createroute":
            return CreateRouteCommand(
                params,
                self._app_data,
                self._route_service,
                self._vehicle_service
            )
            
        if cmd == "unassignedpackages":
            return UnassignedPackagesCommand(
                params,
                self._app_data,
                self._package_service
            )
        
        if cmd == "hubsinfo":
            return HubInfoCommand(
                params,
                self._app_data,
                self._hub_service
            )
            
        if cmd == "inspecthub":
            return InspectHubCommand(
                params,
                self._app_data,
                self._hub_service
            )

        if cmd == "packageinfo":
            return PackageInfoCommand(
                params,
                self._app_data,
                self._package_service,
                self._route_service
            )

        if cmd == "routeinfo":
            return RouteInfoCommand(
                params,
                self._app_data,
                self._route_service,
            )
        
        if cmd == "advanceroutes":
            return AdvanceRoutesCommand(
                params,
                self._app_data,
                self._route_service
            )

        raise ValueError(f"Invalid command name: {cmd}!")