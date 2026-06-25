from datetime import datetime, timedelta

from models.route.route_stop import RouteStop
from enums.route_status import RouteStatus
from models.route.city_graph import CityGraph


class Route:
    
    ### Route class represent a delivery route between multiple locations
    ### It stores stops, assigned truck and packages.
    ### It also provides logic for route validation and delivery checks
    
    def __init__(self, route_id: int, stops: list[RouteStop]):
        if len(stops) < 2:
            raise ValueError("A route must have at least two stops.")

        self.route_id = route_id
        self.stops = stops
        
        # status of route starts as planned
        self.status = RouteStatus.PLANNED

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

    def calculate_total_distance(self) -> int:
        total = 0

        # sum the distance between every two consecutive stops
        for i in range(len(self.stops) - 1):
            total += CityGraph.distance(
                self.stops[i].location,
                self.stops[i + 1].location
            )

        return total

    def calculate_eta(
        self,
        start_time: datetime,
        stop_duration_hours: int = 1
    ):
        # first stop is the route starting point
        self.stops[0].arrival_time = start_time
        self.stops[0].departure_time = start_time

        for i in range(1, len(self.stops)):
            previous_stop = self.stops[i - 1]
            current_stop = self.stops[i]

            distance = CityGraph.distance(
                previous_stop.location,
                current_stop.location
            )

            travel_hours = CityGraph.travel_time_hours(distance)

            arrival_time = (
                previous_stop.departure_time
                + timedelta(hours=travel_hours)
            )

            current_stop.arrival_time = arrival_time
            current_stop.departure_time = (
                arrival_time
                + timedelta(hours=stop_duration_hours)
            )

    def get_current_stop(self, current_time: datetime):
        current_stop = None

        # find the last stop reached by the current time
        for stop in self.stops:
            if (
                stop.arrival_time is not None
                and stop.arrival_time <= current_time
            ):
                current_stop = stop
            else:
                break

        return current_stop

    def __str__(self):
        return f"Route {self.route_id}: {self.start_location} -> {self.end_location}"