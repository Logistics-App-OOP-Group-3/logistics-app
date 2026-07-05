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
        
        hub = self._app_data.find_hub(start_location)
        hub.add_single_package(package)
        
        result = [
            f"Package created successfully.",
            str(package)
            ]
        
        routes = self._route_service.find_routes_for_package(package)
        if routes:
            result.append("Matching routes:")
            for route in routes:
                vehicle = self._app_data.find_vehicle(route.vehicle_id)
                result.append(
                    f"- Route {route.route_id}: "
                    f"{route.route_stops_info(vehicle.max_capacity)}"
                )
        else:
            result.append("No suitable routes")
            result.append(f"Package left at hub {hub.city.value}")
            return "\n".join(result)
        
        print('\n'.join(result))
        
        input_route_id = val_help.try_parse_int(input("Enter route id to assign it to or 0 to leave at hub:\n  "))
        
        if input_route_id != 0:
            for route in routes:
                if route.route_id == input_route_id:
                    self._route_service.assign_package_to_route(package, route.route_id)
                    break
            else:
                raise ValueError("Invalid route_id to assign package to!")
            
            return f"Package assigned to route {input_route_id}"
        return f"Package left at hub {hub.city.value}"
        
        
        
        

