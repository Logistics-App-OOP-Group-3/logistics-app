from __future__ import annotations
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

        self._load_vehicles_from_file()
        self._load_hubs_database()
        
        
        self._app_data.refresh_ids()
    
    def save(self):
        self._file_service.write_lines('vehicles', (v.to_csv() for v in self._app_data.vehicles))   
        #TODO: write other models save      
        
        
        
    ## LOAD METHODS ##
    def _load_hubs_database(self):
        """Currently initialize hubs for every city on program startup"""
        if self._app_data.hubs:
            return

        for c in City:
            self._app_data.add_hub(Hub(c))