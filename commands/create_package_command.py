from __future__ import annotations
from commands.base.base_command import BaseCommand
import commands.validation_helper as val_help

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.package_service import PackageService
    from services.route_service import RouteService
    from core.application_data import ApplicationData

class CreatePackageCommand(BaseCommand):
    def __init__(
        self,
        params,
        app_data: ApplicationData,
        package_service: PackageService,
        route_service :RouteService
    ):
        val_help.validate_params_count(params, 4, "CreatePackageCommand")
        super().__init__(params, app_data)
        self._package_service = package_service
        self._route_service = route_service
    
    def execute(self):
        """ 
            # Dont rush creating package (exhausting package_ids) that the customer
            # might decide to cancel.
            #      opt1: package gets assigned to route
            #      opt2: package is leaved at the hub without route
            #      opt3: the package delivery is canceled
            # 
            # 
        """
        start_location = val_help.try_parse_city(self.params[0])
        end_location = val_help.try_parse_city(self.params[1])
        weight = val_help.try_parse_float(self.params[2])
        contact_info = self.params[3]
        
        package = self._package_service.create_package(
            start_location,
            end_location,
            weight,
            contact_info
        )
        routes = self._route_service.find_routes_for_package(package)
        result = [
            "Package created.",
            f"Package ID: {package.package_id}",
            f"From: {start_location} -> To: {end_location}",
            f"Weight: {weight} kg"
        ]
        
        if routes:
            result.append("Matching routes:")
            for route in routes:
                result.append(
                    f"- Route {route.route_id}: "
                    f"{route.start_location} -> {route.end_location}"
                )
        else:
            result.append("No suitable routes")
            
  
        return "\n".join(result)#

        

