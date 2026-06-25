from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count


class AssignTruckToRouteCommand(BaseCommand):

    def __init__(self, params, app_data, route_service):
        # Expected input: <route_id> <vehicle_id>
        validate_params_count(params, 2)
        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):

        route_id = int(self.params[0])
        vehicle_id = int(self.params[1])

        # Assigns a vehicle (truck) to a route
        # This should:
        # - validate that route exists
        # - validate that vehicle exists
        # - ensure route does not already have a truck
        # - ensure vehicle is not already assigned elsewhere
        # - check capacity and range constraints

        self._route_service.assign_truck_to_route(route_id, vehicle_id)

        return f"Truck {vehicle_id} assigned to route {route_id}"