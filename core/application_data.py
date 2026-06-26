
from typing import TYPE_CHECKING
from core.database_service import DatabaseService
from models.vehicle import Vehicle
if TYPE_CHECKING:
    from models.route.route import Route 
    from models.package.package import Package

# This class holds all objects from our models classes
# And is reponsible for creating UID's
class ApplicationData:
    def __init__(self):
        self._id_package = 0 # UID for creating package
        self._id_routes = 0   # UID for creating route
        self._packages: dict[int, Package] = dict()
        self._routes: dict[int,Route] = dict()
        self._vehicles: dict[int, Vehicle] = dict()
        self._db = DatabaseService()
        self._load_vehicle_database()
        
    @property             # vehicles
    def vehicles(self):
        return tuple(self._vehicles.values())
    @property
    def packages(self):
        return self._packages
    @property
    def routes(self):
        return self._routes
    
# ID GENERATORS
    def generate_package_id(self):
        self._id_package += 1
        return self._id_package
    def generate_route_id(self):
        self._id_routes += 1
        return self._id_routes
    

    
# FIND METHODS
    def find_package(self, id:int) -> Package:
        if id not in self._packages:
            raise ValueError(f"Package id: {id} cannot be found in the system.")
        return self._packages[id]
    
    def find_route(self, id:int) -> Route:
        if id not in self._routes:
            raise ValueError(f"Route id: {id} cannt be found in the system.")
        return self._routes[id]
    
    def find_vehicle(self, id:int) -> Vehicle:
        if id not in self._vehicles:
            raise ValueError(f"Vehicle id: {id} cannot be found in the system.")
        return self._vehicles[id]

# ADD METHODS
    def add_route(self, route: Route):
        self._routes[route.route_id] = route
        
    def add_package(self, package: Package):
        self._packages[package.package_id] = package
    
    def add_vehicle(self, vehicle: Vehicle):
        self._vehicles[vehicle.id] = vehicle 
    
# LOAD DB FROM INITIALIZER METHODS
    def _load_vehicle_database(self):
        for vehicle_model_line in self._db.read_lines('vehicles'):
            vehicle_model_range, *params = vehicle_model_line.split(',')
            start, end = vehicle_model_range.split('-')
            for i in range(int(start), int(end) + 1):
                vehicle = Vehicle.from_csv(f"{i},{','.join(params)}")
                self.add_vehicle(vehicle)
        
    

    
    

    
    