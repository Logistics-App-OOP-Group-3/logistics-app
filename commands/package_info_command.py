from __future__ import annotations
from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count, try_parse_int
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.package_service import PackageService
    from services.route_service import RouteService


class PackageInfoCommand(BaseCommand):

    def __init__(self, params, app_data, package_service: "PackageService", route_service: "RouteService"):
        # Expected input: <package_id>
        validate_params_count(params, 1, "PackageInfoCommand")
        super().__init__(params, app_data)
        self._package_service = package_service
        self._route_service = route_service

    def execute(self):
        package_id = try_parse_int(self.params[0])
        package = self._package_service.get_package(package_id)

        result = [str(package)]
        
        if package.route_id is not None:
            arival_eta = self._route_service.get_eta_for_location(package.route_id, package.end_location)
            result.append(f"Expected arrival time: {arival_eta:%d/%m/%Y %H:%M}")
        return '\n'.join(result)