from __future__ import annotations
from models.route.route import Route
from enums.route_status import RouteStatus
from datetime  import datetime

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

    def create_route(self, stops: list, start_time: datetime = None):
        route_id = self._app_data.generate_route_id()
        
        route = Route(route_id, stops, start_time)
          
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
        
        if route.vehicle_id is None:
            raise ValueError("Route has no vehicle assigned")
        

        vehicle = self._app_data.find_vehicle(route.vehicle_id)
        # check for truck capacity between package start & end location
        # accounting for already assigned packages that are not picked up
        for i in range(pickup_index, dropoff_index):  
            if route.weight_at_stop(i) + package.weight > vehicle.max_capacity:
                raise ValueError(
                    f"Package exceeds vehicle capacity at stop {route.stops[i].location.name}"
                )

        route.add_package(package.package_id)
        package.assign_to_route(route.route_id)
        pickup_stop.add_pick_up_weigth(package.weight)
        dropoff_stop.add_drop_off_weigth(package.weight)



    def assign_packages_from_hubs(self, route: Route, vehicle: Vehicle):
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
            current_weight = route.weight_at_stop(i)

            for package in candidates:
                if current_weight + package.weight > vehicle.max_capacity:
                    continue  # skip this package, maybe next one will fit
                
                current_weight += package.weight
                pickup_stop = stops[i]

                dropoff_stop = next((s for s in stops if s.location == package.end_location), None)

                # Niki cod 
                if dropoff_stop is None:
                    raise ValueError(f"Route is invalid: missing stop for {package.end_location} I told you so"
                                     f"Trqbva qko da gurmi. Programata da krashne.")

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
        
    # SIMULATION FUNC
    def complete_all_routes_next_stop(self):
        """Simulation func": that executes the completion of route's next stop"""
        for route in self.get_routes_by_status(RouteStatus.IN_PROGRESS):
            stop_idx = route.get_index_of_next_incompleted_stop()
            
            if stop_idx == 0: # first stop
                self.load_route_packages_from_stop(route, stop_idx)
            elif stop_idx == len(route.stops) - 1: # last stop
                self.unload_route_packages_from_stop(route, stop_idx)
                self.mark_route_as_completed(route)
            else:
                self.unload_route_packages_from_stop(route, stop_idx)
                self.load_route_packages_from_stop(route, stop_idx)
                
            self.mark_stop_as_completed(route, stop_idx)
                

    def load_route_packages_from_stop(self, route: Route, stop_index: int):
        stop = route.stops[stop_index]
        hub = self._app_data.find_hub(stop.location)
        
        for package_id in route.packages_ids:
            if package_id in hub.packages_ids:
                hub.remove_single_package(package_id)
    
    def unload_route_packages_from_stop(self, route: Route, stop_index: int):
        stop = route.stops[stop_index]
        hub = self._app_data.find_hub(stop.location)
        
        for package_id in route.packages_ids:
            package = self._app_data.find_package(package_id)
            if package.end_location == hub.city:
                hub.add_single_package(package, delivered=True)
        
    def mark_route_as_completed(self, route: Route):
        if route.status != RouteStatus.IN_PROGRESS:
            raise ValueError("Only routes in progress can be completed")
        
        route.status = RouteStatus.COMPLETED
        
    def mark_stop_as_completed(self,route :Route , stop_index: int):
        stops = route.stops
        if not 0 <= stop_index < len(stops):
            raise ValueError(f"Route stop index [{stop_index}] out bound!")
        if stops[stop_index].stop_status == RouteStatus.COMPLETED:
            raise ValueError(f"Cannot mark stop as completed: Route stop [{stop_index}] already completed!")
        stops[stop_index].stop_status = RouteStatus.COMPLETED    
        
    def get_routes_by_status(self, status: RouteStatus):
        return [
            route
            for route in self._app_data.routes.values()
            if route.status == status
        ]
    def get_routes_in_progress(self):
        return self.get_routes_by_status(RouteStatus.IN_PROGRESS)
