from datetime import datetime, timedelta
from models.route.route_stop import RouteStop
from enums.route_status import RouteStatus
from models.route.city_graph import CityGraph

class Route:
    """
    Route class represents a delivery route between multiple locations.
    It stores stops, assigned truck and packages.
    It also provides logic for route validation and delivery checks.
    """
    MAX_DISTANCE = 13000
    
    # Added optional start_time parameter to support explicit departure planning (Use Case #2)
    def __init__(self, route_id: int, stops: list[RouteStop], start_time: datetime = None):
        if len(stops) < 2:
            raise ValueError("A route must have at least two stops.")

        self._route_id = route_id
        self._vehicle_id = None
        self._packages_ids: set[int] = set() 
        self._status = RouteStatus.PLANNED 
        self._stops: list[RouteStop] = stops

        self._total_distance = self._calculate_total_distance()
        
        if start_time is None:
            start_time = datetime.now()
            
        self._calculate_stops_eta(start_time)
        
    @property                         
    def route_id(self):
        return self._route_id
        
    @property                         
    def vehicle_id(self):
        return self._vehicle_id
        
    @vehicle_id.setter                
    def vehicle_id(self, value: int):
        self._vehicle_id = value
        
    @property                         
    def total_distance(self):
        return self._total_distance
        
    @property                         
    def packages_ids(self): 
        return tuple(self._packages_ids)
        
    @property                         
    def status(self):
        return self._status
        
    @status.setter
    def status(self, value: RouteStatus):
        self._status = value
        
    @property                         
    def stops(self):
        return tuple(self._stops)
    
    @property                         
    def start_location(self):
        return self._stops[0].location
    
    @property
    def current_location(self) -> str | None:
        """Last completed city"""
        last_stop = None
        for stop in self._stops:
            if stop.stop_status == RouteStatus.COMPLETED:
                last_stop = stop
        return last_stop.location.value if last_stop is not None else None
        
    @property                         
    def end_location(self):
        return self._stops[-1].location
        
    @property   
    def locations(self):
        return [stop.location for stop in self._stops]
    

    def can_deliver_between(self, start_location: str, end_location: str) -> bool:
        """Is
            param[0]: package: start_location
        before
            param[1]: package: end_location
        in route stop.
        """
        if start_location not in self.locations or end_location not in self.locations:
            return False
        
        return self.locations.index(start_location) < self.locations.index(end_location)

    def add_package(self, package_id: int):
        if package_id in self._packages_ids:
            raise ValueError(f"Cannot add existing package [{package_id}] to the route")
        self._packages_ids.add(package_id)
      
    def get_index_of_next_incompleted_stop(self) -> int:
        """ Returns: index of first incompleted route_stop """
        for i in range(len(self._stops)):
            if self._stops[i].stop_status == RouteStatus.IN_PROGRESS:
                return i
        raise ValueError("Searching for incompleted stop in a completed route.")
        
    # CURRENTLY IGNORED FUNC
    # DUE TO THE SIMULATION OF COMPLETING ROUTE STOPS
    def get_current_stop(self, current_time: datetime):
        current_stop = None
        for stop in self.stops:
            if stop.arrival_time is not None and stop.arrival_time <= current_time:
                current_stop = stop
            else:
                break
        return current_stop

    def weight_at_stop(self, stop_index: int) -> float:
        weight = 0
        for stop in self._stops[:stop_index + 1]:
            weight = round(weight + stop.pick_up_weight, 2)
            weight = round(weight - stop.drop_off_weight, 2)
        return weight

    def calculate_stops_capacity(self):
        """
            List with packages weight at each stop after unloading delivered packages
            and loading packages for the next stops in the route.
        """
        
        return [self.weight_at_stop(i) for i in range(len(self._stops))]

    #Brisbane (Oct 10th 06:00h) → Sydney (Oct 10th 20:00h) → Melbourne (Oct 11th 18:00h)
    def route_stops_info(self, vehicle_max_capacity: int = None):
        
        def ordinal_suffix(day):
            if 11 <= day <= 13:
                return "th"
            return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        
        def format_dt(dt: datetime):
            day = dt.day
            suffix = ordinal_suffix(day)
            return f"({dt.strftime('%b')} {day}{suffix} {dt.strftime('%H:%M')}h)"
        
        result = []
        stops_capacity = self.calculate_stops_capacity()
        for stop, capacity in zip(self._stops, stops_capacity):
            line = f"{stop.location.value} {format_dt(stop.arrival_time)}"
            if vehicle_max_capacity:
                free_capacity = vehicle_max_capacity - capacity
                line += f" Free: [{free_capacity} kg]"
            result.append(line)
        return ' -> '.join(result)

    def __str__(self):
        result = [f"Route {self._route_id}: {' -> '.join(c.value for c in self.locations)}"]
        result.append(f"Status: {self.status.value}")
        result.append(f"Vehicle ID: {self._vehicle_id}")
        if self.status != RouteStatus.COMPLETED:
            location = self.current_location
            if location is None:
                result.append(f"Location: On the way to the first location")
            else:
                result.append(f"Location: {location}")
               
        result.append("-stops info-")
        for index, stop in enumerate(self._stops):
            result.append(f'  {stop} | Truck load: {self.weight_at_stop(index):.2f} kg')
        return '\n'.join(result)

    def _calculate_stops_eta(self, start_time: datetime, stop_duration_hours: int = 1):
        self._stops[0].arrival_time = start_time
        self._stops[0].departure_time = start_time + timedelta(hours=stop_duration_hours)
        self._stops[0].stop_status = RouteStatus.IN_PROGRESS
        for i in range(1, len(self._stops)):
            previous_stop = self._stops[i - 1]
            current_stop = self._stops[i]

            distance = CityGraph.distance(
                previous_stop.location,
                current_stop.location
            )

            travel_hours = CityGraph.travel_time_hours(distance)
            arrival_time = previous_stop.departure_time + timedelta(hours=travel_hours)

            current_stop.arrival_time = arrival_time
            current_stop.departure_time = arrival_time + timedelta(hours=stop_duration_hours)
            
    def _calculate_total_distance(self) -> int:
        total = 0
        for i in range(len(self._stops) - 1):
            total += CityGraph.distance(
                self._stops[i].location,
                self._stops[i + 1].location
            )
        if total > self.MAX_DISTANCE:
            raise ValueError(f"Route distance cannot exceed: {self.MAX_DISTANCE}")
        return total