from commands.base.base_command import BaseCommand
from models.route.route_stop import RouteStop


class CreateRouteCommand(BaseCommand):

    def __init__(self, params, app_data, route_service):
        if len(params) < 2:
            raise ValueError("A route must have at least two stops")

        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):

        stops = [
            RouteStop(location)
            for location in self.params
        ]

        route = self._route_service.create_route(stops)

        return (
            f"Route created successfully.\n"
            f"Route ID: {route.route_id}\n"
            f"Stops: {' -> '.join(route.locations)}"
        )