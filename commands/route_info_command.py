from __future__ import annotations
from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count, try_parse_int
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.route_service import RouteService

class RouteInfoCommand(BaseCommand):

    def __init__(self, params, app_data, route_service :"RouteService"):
        # Expected input: <route_id>
        validate_params_count(params, 1, "RouteInfoCommand")
        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):

        route_id = try_parse_int(self.params[0])
        route = self._route_service.get_route(route_id)
        
        result = [str(route)]
        vehicle = self.app_data.find_vehicle(route.vehicle_id)
        result.append(f"{"":<56}Max capaci: {vehicle.max_capacity} kg")
        if not route.packages_ids:
            result.append('Packages: No packages have been assigned to this route.')
        else:
            result.append(f"Packages: {', '.join(map(str, route.packages_ids))}")

        return '\n'.join(result)