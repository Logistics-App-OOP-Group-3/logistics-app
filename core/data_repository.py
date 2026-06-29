from core.file_service import FileService
from models.package.package import Package
from models.route.route import Route
from models.vehicle import Vehicle
from models.hub import Hub
from enums.city import City
from commands.validation_helper import validate_params_count

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.application_data import ApplicationData


class DataRepository:
    
    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data
        self._file_service = FileService()
        
        
    def load(self):
        max_package_id = 0
        max_route_id = 0
        max_vehicle_id = self._load_vehicles_from_file()
        self._load_hubs_database()
        
        self._app_data.sync_ids(max_package_id, max_route_id, max_vehicle_id)
    
    def save(self):
        self._file_service.write_lines('vehicles', (v.to_csv() for v in self._app_data.vehicles))   
        #TODO: write other models save      
        
        
        
    ## LOAD METHODS ##
    def _load_vehicles_from_file(self) -> int:
        """ Returns max_vehicle_id loaded from the file"""
        max_vehicle_id = 0
        for vehicle_model_line in self._file_service.read_lines('vehicles'):
            params = vehicle_model_line.split(',')
            validate_params_count(params, 4, "Load vehicle from file")
            
            vehicle = Vehicle.from_csv(vehicle_model_line)
            max_vehicle_id = max(max_vehicle_id, vehicle.vehicle_id)
            self._app_data.add_vehicle(vehicle)
        return max_vehicle_id
    
    def _load_hubs_database(self):
        """Currently initialize hubs for every city on program startup"""
        for c in City:
            self._app_data.add_hub(Hub(c))