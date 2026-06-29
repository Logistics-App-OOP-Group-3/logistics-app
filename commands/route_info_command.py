from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count


class RouteInfoCommand(BaseCommand):

    def __init__(self, params, app_data, route_service):
        # Expected input: <route_id>
        validate_params_count(params, 1, "RouteInfoCommand")
        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):

        route_id = int(self.params[0])

        # Displays detailed route information
        # Should include:
        # - route stops
        # - assigned truck
        # - assigned packages
        # - route status

        route = self._route_service.get_route(route_id)

        return str(route)