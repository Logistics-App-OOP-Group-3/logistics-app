from models.route_stop import RouteStop

class Route:
    def __init__(self, route_id: int, stops: list[RouteStop]):
                
        if len(stops) < 2:
            raise ValueError("A route must contain at least two stops.")
        
        self.route_id = route_id
        self.stops = stops
        
        self.truck_id = None
        self.package_ids = []
        
        #self.total_distance = 0
        
    @property
    def start_location(self):
        return self.stops[0].location
    
    @property
    def end_location(self):
        return self.stops[-1].location
    
    def assign_truck(self, truck_id: int):
        self.truck_id = truck_id
        
    def add_package(self, package_id: int):
        if package_id not in self.package_ids:
            self.package_ids.append(package_id)
            
            
    def can_deliver_between(self, start_location: str, end_location: str) -> bool:
        locations = [stop.location for stop in self.stops]
        
        if start_location not in locations:
            return False
        if end_location not in locations:
            return False
        
        return locations.index(start_location) < locations.index(end_location)
    
    def get_locations(self):
        return [stop.location for stop in self.stops]
    

    def __str__(self):
        return f"Route {self.route_id}: {self.start_location} -> {self.end_location}"