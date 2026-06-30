from __future__ import annotations
from models.route.route import Route
from enums.route_status import RouteStatus
from enums.package_status import PackageStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.package.package import Package
    from core.application_data import ApplicationData
    from models.vehicle import Vehicle

class RouteService:
    
    ### Handles all business logic related to routes
    ### Respponsible for creating routes, finding matching routes for packages and assigning packages and trucks
    
    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data

    def create_route(self, stops: list):
        route_id = self._app_data.generate_route_id()
        
        route = Route(route_id, stops)
          
        return route

    def get_route(self, route_id: int) -> Route:
        return self._app_data.find_route(route_id)
    
    def get_all_routes(self):
        return list(self._app_data.routes.values())

    def find_routes_for_package(self, package: Package):

        return [
            route
            for route in self._app_data.routes.values()
            if route.can_deliver_between(
                package.start_location,
                package.end_location
            )
        ]
        
    def assign_package_to_route(self, package: Package, route_id: int):
        """
        Assign package to route only if there is enough space
        from starting to end point. Accounting for packages that are not
        currently picked up, but are already assigned.
        """
        route = self.get_route(route_id)

        if package.route_id is not None:
            raise ValueError("Package already assigned")

        if not route.can_deliver_between(
            package.start_location,
            package.end_location
        ):
            raise ValueError("Route cannot deliver this package")

        pickup_stop = next(s for s in route.stops if s.location == package.start_location)
        dropoff_stop = next(s for s in route.stops if s.location == package.end_location)
        pickup_index = route.stops.index(pickup_stop)
        dropoff_index = route.stops.index(dropoff_stop)
        
        vehicle = self._app_data.find_vehicle(route.vehicle_id)
        # check for truck capacity between package start & end location
        # accounting for already assigned packages that are not picked up
        for i in range(pickup_index, dropoff_index):  
            if route.weight_at_stop(i) + package.weight > vehicle.capacity:
                raise ValueError(
                    f"Package exceeds vehicle capacity at stop {route.stops[i].location.name}"
                )

        route.add_package(package.package_id)
        package.assign_to_route(route.route_id)
        pickup_stop.add_pick_up_weigth(package.weight)
        dropoff_stop.add_drop_off_weigth(package.weight)



    def load_packages_from_hubs(self, route: Route, vehicle: Vehicle):
        """
        For each stop, find unassigned packages at that hub
        destined for any later stop, then load them in acceptance order
        up to the vehicle's remaining capacity.
        """
        stops = route.stops

        for i in range(len(stops) - 1):
            hub = self._app_data.find_hub(stops[i].location)
            later_stops = [stop.location for stop in stops[i+1::]]
            candidates = hub.find_packages_for_locations(later_stops)
            current_weigth = route.weight_at_stop(i)

            for package in candidates:
                if current_weigth + package.weight > vehicle.capacity:
                    continue  # skip this package, maybe next one will fit
                
                current_weigth += package.weight
                pickup_stop = stops[i]

                dropoff_stop = next(s for s in stops if s.location == package.end_location)

                route.add_package(package.package_id)
                package.assign_to_route(route.route_id)
                pickup_stop.add_pick_up_weigth(package.weight)
                dropoff_stop.add_drop_off_weigth(package.weight)



    def assign_truck_to_route(self, route: Route, vehicle: Vehicle):
        
        if route.vehicle_id is not None:
            raise ValueError("Route already has a truck")
        
        if vehicle.route_id is not None:
            raise ValueError("Truck already assigned")

        route.vehicle_id = vehicle.vehicle_id
        vehicle.route_id = route.route_id

    def start_route(self, route_id: int):
        route = self.get_route(route_id)
        
        if route.vehicle_id is None:
            raise ValueError("Cannot start a route without a truck assigned to it")
        
        if route.status == RouteStatus.COMPLETED:
            raise ValueError("Cannot start a route that is completed")
        
        route.status = RouteStatus.IN_PROGRESS
        
        
    def complete_route(self, route_id: int):
        route = self.get_route(route_id)
        
        if route.status != RouteStatus.IN_PROGRESS:
            raise ValueError("Only routes in progress can be completed")
        
        route.status = RouteStatus.COMPLETED
        
    def get_routes_by_status(self, status: RouteStatus):
        return [
            route
            for route in self._app_data.routes.values()
            if route.status == status
        ]
    def get_routes_in_progress(self):
        return self.get_routes_by_status(RouteStatus.IN_PROGRESS)
