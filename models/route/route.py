from datetime import datetime, timedelta

from models.route.route_stop import RouteStop
from enums.route_status import RouteStatus
from models.route.city_graph import CityGraph


class Route:
    
    ### Route class represent a delivery route between multiple locations
    ### It stores stops, assigned truck and packages.
    ### It also provides logic for route validation and delivery checks
    
    MAX_DISTANCE = 13000
    
    def __init__(self, route_id: int, stops: list[RouteStop]):
        if len(stops) < 2:
            raise ValueError("A route must have at least two stops.")

        #todo: remove todos: All done
        #TODO: encapsulate                                                     -=- DONE
        #TODO: Adding total_distance attribute will simplify outside logic     -=- DONE
        #TODO: Also assigning expected arival times on creation                -=- DONE
        #TODO: Departure time can be simply 30 min or 1h for loading/unloading -=- DONE
        
        self._route_id = route_id
        self._vehicle_id = None
        self._packages_ids: list[int] = []
        self._status = RouteStatus.PLANNED # status of route starts as planned
        self._stops: list[RouteStop] = stops
        self._total_distance = self._calculate_total_distance()
        self._calculate_stops_eta(datetime.now())
        
## PROPERTIES
    @property                         # route_id
    def route_id(self):
        return self._route_id
    @property                         # vehicle_id
    def vehicle_id(self):
        return self._vehicle_id
    @vehicle_id.setter                # vehicle_id
    def vehicle_id(self, value: int):
        self._vehicle_id = value
    @property                         # total_distance
    def total_distance(self):
        return self._total_distance
    @property                         # packages_ids
    def packages_ids(self): 
        return tuple(self._packages_ids)
    @property                         # status
    def status(self):
        return self._status
    #TODO: status setter or other method for status change
    @property                         # stops
    def stops(self):
        return tuple(self._stops)
    
    @property                         # calculated
    def start_location(self):
        return self._stops[0].location
    @property                         # calculated
    def end_location(self):
        return self._stops[-1].location
    @property                         # calculated   
    def locations(self):
        return [stop.location for stop in self._stops]
    
    #TODO: property ?  -=- DONE
    # def assign_truck(self, truck_id: int): 
    #     self.truck_id = truck_id


## PUBLIC METHODS
    def can_deliver_between(self, start_location: str, end_location: str) -> bool:
        if start_location not in self.locations:
            return False

        if end_location not in self.locations:
            return False

        return self.locations.index(start_location) < self.locations.index(end_location)


    def add_package(self, package_id: int):
        if package_id not in self._packages_ids: #TODO: to many list index search overhead/ since we ignore duplicate we can simply use set
            self._packages_ids.append(package_id)


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

## PRIVATE METHODS
    def __str__(self):
        return (
            f"Route {self._route_id}: {' -> '.join(c.value for c in self.locations)}\n"
            f"{'\n'.join(str(stop) for stop in self._stops)}"
            )
    
    def _calculate_stops_eta(
        self,
        start_time: datetime,
        stop_duration_hours: int = 1
    ):
        """
        Calculates and assigns all RouteStops:
            Departure Time
            Arrival Time
        param[0] = arival time for first stop
        param[1] = delay after ariving at one stop and leaving for the next one
        """
        # first stop is the route starting point
        self.stops[0].arrival_time = start_time
        self.stops[0].departure_time = start_time + timedelta(hours=stop_duration_hours)

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

    def _calculate_total_distance(self) -> int:
        """ Sum distance between each route stop """
        total = 0
        # sum the distance between every two consecutive stops
        for i in range(len(self.stops) - 1):
            total += CityGraph.distance(
                self.stops[i].location,
                self.stops[i + 1].location
            )
        if total > self.MAX_DISTANCE:
            raise ValueError(f"Route distance cannot exceed: {self.MAX_DISTANCE}")
        return total