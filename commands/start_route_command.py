from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count


class StartRouteCommand(BaseCommand):

    def __init__(self, params, app_data, route_service):
        # Expected input: <route_id>
        validate_params_count(params, 1, "StartRouteCommand")
        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):

        route_id = int(self.params[0])

        # Starts execution of a route
        # This should:
        # - verify route exists
        # - ensure route has a truck assigned
        # - ensure route is in PLANNED state
        # - change status to IN_PROGRESS

        self._route_service.start_route(route_id)

        return f"Route {route_id} started"