from models.route.route import Route

class RouteService:
    
    ### Handles all business logic related to routes
    ### Respponsible for creating routes, finding matching routes for packages and assigning packages and trucks
    
    def __init__(self, app_data):
        self.app_data = app_data

    def create_route(self, route_id: int, stops: list):
        if route_id in self.app_data.routes:
            raise Exception("Route already exists")

        route = Route(route_id, stops)
        self.app_data.routes[route_id] = route

        return route

    def get_route(self, route_id: int):
        if route_id not in self.app_data.routes:
            raise Exception("Route not found")

        return self.app_data.routes[route_id]

    def find_routes_for_package(self, package):
        matching_routes = []

        for route in self.app_data.routes.values():
            if route.can_deliver_between(
                package.start_location,
                package.end_location
            ):
                matching_routes.append(route)

        return matching_routes

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

    def get_all_routes(self):
        return list(self.app_data.routes.values())