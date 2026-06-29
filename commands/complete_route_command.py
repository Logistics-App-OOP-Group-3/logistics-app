from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count


class CompleteRouteCommand(BaseCommand):

    def __init__(self, params, app_data, route_service):
        # Expected input: <route_id>
        validate_params_count(params, 1, "CompleteRouteCommand")
        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):

        route_id = int(self.params[0])

        # Completes a route
        # This should:
        # - verify route exists
        # - ensure route is IN_PROGRESS
        # - mark route as COMPLETED
        # - optionally trigger package delivery updates

        self._route_service.complete_route(route_id)

        return f"Route {route_id} completed"