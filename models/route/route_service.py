from models.route.route import Route
from models.route.route_status import RouteStatus
class RouteService:
    
    ### Handles all business logic related to routes
    ### Respponsible for creating routes, finding matching routes for packages and assigning packages and trucks
    
    def __init__(self, app_data):
        self.app_data = app_data

    def create_route(self, stops: list):
        route_id = self.app_data.generate_route_id()
        
        route = Route(route_id, stops)
        
        self.app_data.add_route(route)
        return route

    def get_route(self, route_id: int):
        return self.app_data.find_route(route_id)
    
    def get_all_routes(self):
        return list(self.app_data.routes.values())

    def find_routes_for_package(self, package):

        return [
            route
            for route in self.app_data.routes.values()
            if route.can_deliver_between(
                package.start_location,
                package.end_location
            )
        ]
        
    def assign_package_to_route(self, package, route_id: int):
        route = self.get_route(route_id)

        if package.route_id is not None:
            raise Exception("Package already assigned")

        if not route.can_deliver_between(
            package.start_location,
            package.end_location
        ):
            raise Exception("Route cannot deliver this package")

        route.add_package(package.package_id)
        package.route_id = route.route_id

    def assign_truck_to_route(self, route_id: int, truck):
        route = self.get_route(route_id)

        if route.truck_id is not None:
            raise Exception("Route already has a truck")

        if truck.assigned_route is not None:
            raise Exception("Truck already assigned")

        route.assign_truck(truck.vehicle_id)
        truck.assigned_route = route.route_id

    def start_route(self, route_id: int):
        route = self.get_route(route_id)
        
        if route.truck_id is None:
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
            for route in self.app_data.routes.values()
            if route.status == status
        ]
    def get_routes_in_progress(self):
        return self.get_routes_by_status(RouteStatus.IN_PROGRESS)
