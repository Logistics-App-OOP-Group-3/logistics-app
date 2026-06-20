from models.route.route_stop import RouteStop


class Route:
    
    ### Route class represent a delivery route between multiple locations
    ### It stores stops, assigned truck and packages.
    ### It also provides logic for route validation and delivery checks
    
    def __init__(self, route_id: int, stops: list[RouteStop]):
        if len(stops) < 2:
            raise ValueError("A route must have at least two stops.")

        self.route_id = route_id
        self.stops = stops

        self.truck_id = None
        self.package_ids = []

    @property
    def start_location(self):
        return self.stops[0].location

    @property
    def end_location(self):
        return self.stops[-1].location

    @property
    def locations(self):
        return [stop.location for stop in self.stops]

    def can_deliver_between(self, start_location: str, end_location: str) -> bool:
        if start_location not in self.locations:
            return False
        if end_location not in self.locations:
            return False

        return self.locations.index(start_location) < self.locations.index(end_location)

    def add_package(self, package_id: int):
        if package_id not in self.package_ids:
            self.package_ids.append(package_id)

    def assign_truck(self, truck_id: int):
        self.truck_id = truck_id

    def __str__(self):
        return f"Route {self.route_id}: {self.start_location} -> {self.end_location}"