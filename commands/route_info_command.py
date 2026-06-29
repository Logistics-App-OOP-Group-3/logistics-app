from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count


class RouteInfoCommand(BaseCommand):

    def __init__(self, params, app_data, route_service, vehicle_service):
        # Expected input: <route_id>
        validate_params_count(params, 1)
        super().__init__(params, app_data)
        self._route_service = route_service
        self._vehicle_service = vehicle_service

    def execute(self):

        route_id = int(self.params[0])

        # Displays detailed route information
        # Should include:
        # - route stops
        # - assigned truck
        # - assigned packages
        # - route status

        route = self._route_service.get_route(route_id)
        
        result = [str(route),
                  f'Status: {route.status.value}'
                  ]

        if route.vehicle_id is None:
            result.append('Assigned truck: Not Assigned')
        else:
            result.append(f'Assigned truck: {route.vehicle_id}')

        if not route.packages_ids:
            result.append('Packages: No packages have been assigned to this route.')
        else:
            result.append(f"Packages: {', '.join(map(str, route.packages_ids))}")

        return '\n'.join(result)