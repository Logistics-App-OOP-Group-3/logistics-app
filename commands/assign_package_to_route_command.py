from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count


class AssignPackageToRouteCommand(BaseCommand):

    def __init__(self, params, app_data, route_service, package_service):
        # Expected input: <package_id> <route_id>
        validate_params_count(params, 2)
        super().__init__(params, app_data)
        self._route_service = route_service
        self._package_service = package_service

    def execute(self):

        package_id = int(self.params[0])
        route_id = int(self.params[1])

        # Assigns a package to a route
        # This should:
        # - ensure package exists
        # - ensure route exists
        # - ensure package is not already assigned
        # - validate route can deliver between package start/end locations
        # - update both route and package state

        self._route_service.assign_package_to_route(package_id, route_id)

        return f"Package {package_id} assigned to route {route_id}"