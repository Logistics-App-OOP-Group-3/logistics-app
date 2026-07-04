from commands.base.base_command import BaseCommand
from models.route.route_stop import RouteStop
from services.route_service import RouteService
from services.vehicle_service import VehicleService
import commands.validation_helper as vh

class CreateRouteCommand(BaseCommand):

    def __init__(self, params, app_data, route_service: RouteService, vehicle_service: VehicleService):
        super().__init__(params, app_data)
        self._route_service = route_service
        self._vehicle_service = vehicle_service


    def execute(self):
        """
        CREATE route with stops      (route_service)[init all stop departure & arival time]
        SEACH for available vehicle  (vehicle_service)
        DISCARD route if no vehicle to complete it AND raise error
        ADD packages from hubs (FIFO) calculating how much is droped off and picked up at each stop
        """
        stops = [
            RouteStop(vh.try_parse_city(location))
            for location 
            in self.params
            ]
        
        route = self._route_service.create_route(stops)
        vehicle = self._vehicle_service.find_available_vehicle_for_distance(route.total_distance)
        
        if not vehicle:
            raise ValueError(
                f"Cannot currently complete route.\n"
                f" -No vehicle available to cover route distance: [{route.total_distance}]"
                )
            
        self._route_service.assign_truck_to_route(route, vehicle)
        self._route_service.assign_packages_from_hubs(route, vehicle)
                        
        self.app_data.add_route(route)
        return (
            f"Route created successfully.\n"
            f"{route}\n"
            f"Vehicle ID: {vehicle.vehicle_id}"
        )