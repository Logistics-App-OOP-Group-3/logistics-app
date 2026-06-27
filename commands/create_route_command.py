from commands.base.base_command import BaseCommand
from models.route.route_stop import RouteStop
from services.route_service import RouteService
from services.vehicle_service import VehicleService

class CreateRouteCommand(BaseCommand):

    def __init__(self, params, app_data, route_service: RouteService, vehicle_service: VehicleService):
        if len(params) < 2:
            raise ValueError("A route must have at least two stops")

        super().__init__(params, app_data)
        self._route_service = route_service
        self._vehicle_service = vehicle_service

    def execute(self):
        """
        CREATE route with stops      (route_service)[init all stop departure & arival time]
        SEACH for available vehicle  (vehicle_service)
        DISCARD route if no vehicle to complete it AND raise error
        TODO: add packages
        
        """
        
        stops = [
            RouteStop(location)
            for location in self.params
        ]

        route = self._route_service.create_route(stops)
        vehicle = self._vehicle_service.available_vehicle_for_distance(route.total_distance)
        
        if not vehicle:
            raise ValueError(
                f"Cannot currently complete route.\n"
                f" -No vehicle available to cover route distance: [{route.total_distance}]"
                )
            
        self._route_service.assign_truck_to_route(route, vehicle)
        
        #TODO: assign packages to route
        
        self.app_data.add_route(route)
        return (
            f"Route created successfully.\n"
            f"{route}"
            f"Vehicle ID: {vehicle.vehicle_id}\n"
            f"Stops: {' -> '.join(route.locations)}"
        )