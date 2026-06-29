from typing import TYPE_CHECKING
from models.vehicle import Vehicle
from models.hub import Hub
from enums.city import City
from services.vehicle_service import VehicleService
if TYPE_CHECKING:
    from models.route.route import Route 
    from models.package.package import Package

# This class holds all objects from our models classes
# And is reponsible for creating UID's
class ApplicationData:
    def __init__(self):
        self._id_package = 0 # UID for creating package
        self._id_route = 0   # UID for creating route
        self._id_vehicle = 0 # UID for creating vehicle
        self._packages: dict[int, Package] = dict()
        self._routes: dict[int,Route] = dict()
        self._vehicles: dict[int, Vehicle] = dict()
        self._hubs: dict[City, Hub] = dict()
        # self._load_vehicle_database()
        # self._load_hubs_database()
        
    @property
    def packages(self):
        return self._packages
    @property
    def routes(self):
        return self._routes
    @property
    def vehicles(self):
        return tuple(self._vehicles.values()) 
    @property
    def hubs(self):
        return tuple(self._hubs.values())
    
    def sync_ids(self, max_package_id: int, max_route_id: int, max_vehicle_id: int):
        self._id_package = max_package_id
        self._id_route = max_route_id
        self._id_vehicle = max_vehicle_id
    
# ID GENERATORS
    def generate_package_id(self):
        self._id_package += 1
        return self._id_package
    def generate_route_id(self):
        self._id_route += 1
        return self._id_route
    def generate_vehicle_id(self):
        self._id_vehicle += 1
        return self._id_vehicle
    
# FIND METHODS
    def find_package(self, id:int) -> Package:
        if id not in self._packages:
            raise ValueError(f"Package id: {id} cannot be found in the system!")
        return self._packages[id]
    
    def find_route(self, id:int) -> Route:
        if id not in self._routes:
            raise ValueError(f"Route id: {id} cannt be found in the system!")
        return self._routes[id]
    
    def find_vehicle(self, id:int) -> Vehicle:
        if id not in self._vehicles:
            raise ValueError(f"Vehicle id: {id} cannot be found in the system!")
        return self._vehicles[id]
    
    def find_hub(self, city: City):
        if city not in self._hubs:
            raise ValueError(f"Hub in City: {city.value} cannot be found in the system!")
        return self._hubs[city]

# ADD METHODS
    def add_route(self, route: Route):
        self._routes[route.route_id] = route
        
    def add_package(self, package: Package):
        self._packages[package.package_id] = package
    
    def add_vehicle(self, vehicle: Vehicle):
        self._vehicles[vehicle.vehicle_id] = vehicle
    
    def add_hub(self, hub: Hub):
        self._hubs[hub.city] = hub
    

            
        
        
    

    
    

    
    