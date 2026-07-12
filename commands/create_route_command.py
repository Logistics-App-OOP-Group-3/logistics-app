from commands.base.base_command import BaseCommand
from models.route.route_stop import RouteStop
from services.route_service import RouteService
from services.vehicle_service import VehicleService
import commands.validation_helper as vh

class CreateRouteCommand(BaseCommand):
    """
    input_trigger: createroute 
        param[0]: date_time [format: Sep-12th-06:00h]
        *params: enum.City  [unique values]
    excetuion:
        CreateRoute with:
            start_time: param[0]
            stops: list[*params]
        SearchVehicle by availability and total route distance
        Assigns packages from hubs in the route's consecutive visit order,
        using FIFO order within each hub.
        Mark route and stops IN_PROGRESS
    """

    def __init__(self, params, app_data, route_service: RouteService, vehicle_service: VehicleService):
        super().__init__(params, app_data)
        self._route_service = route_service
        self._vehicle_service = vehicle_service


    def execute(self):
        # Capitalize the input to match the expected format ("Jan-31-14:30h").
        date_time = vh.try_parse_date_time(self.params[0].capitalize())
        stops = [
            RouteStop(vh.try_parse_city(location))
            for location 
            in self.params[1:]
            ]
        
        route = self._route_service.create_route(stops, date_time)
        vehicle = self._vehicle_service.find_available_vehicle_for_distance(route.total_distance)
        
        if not vehicle:
            raise ValueError(
                f"Cannot currently complete route.\n"
                f" -No vehicle available to cover route distance: [{route.total_distance}]"
                )
            
        self._route_service.assign_truck_to_route(route, vehicle)
        self._route_service.assign_packages_from_hubs(route, vehicle)
        self._route_service.start_route(route) # status init method
                
        # use [result_list + join] to skip '--' separation of message for automatically assigned packages, when none        
        return (
            f"\nRoute created successfully.\n"
            f"--\n"
            f"{'\n'.join(
                [
                    f'Package [{package_id}] assigned to route [{route.route_id}]'
                    for package_id in route.packages_ids
                ]
                )}\n"
            f"--\n"
            f"{route}\n"
        )