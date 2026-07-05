from __future__ import annotations
from core.file_service import FileService
from models.package import Package
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
    
    def save(self):
        self._file_service.write_lines('vehicles', (v.to_csv() for v in self._app_data.vehicles)) 
        # TODO: write other models save      
        
    ## LOAD METHODS ##
    def _load_vehicles_from_file(self):
        """
        Loads vehicles from the vehicles.csv file.
        If the file is empty or missing, it seeds the official company fleet 
        as defined in the requirements spec.
        """
        try:
            lines = list(self._file_service.read_lines('vehicles'))
            if lines:
                for line in lines:
                    if not line.strip():
                        continue
                    # Assuming standard CSV: vehicle_id, name, capacity, max_range, route_id
                    parts = line.strip().split(',')
                    v_id = int(parts[0])
                    name = parts[1]
                    capacity = int(parts[2])
                    max_range = int(parts[3])
                    route_id = int(parts[4]) if (len(parts) > 4 and parts[4] and parts[4] != 'None') else None
                    
                    vehicle = Vehicle(v_id, name, capacity, max_range)
                    if route_id is not None:
                        vehicle.route_id = route_id
                    self._app_data.add_vehicle(vehicle)
                    self._app_data.observe_vehicle_id(v_id)
                return
        except Exception:
            # Fall back to seeding if file operations fail or file doesn't exist yet
            pass

        # Seed official company fleet if CSV was empty or not found
        self._seed_official_fleet()

    def _seed_official_fleet(self):
        """Seeds the 40 official company vehicles per the specification requirements."""
        # 1001-1010: Scania | Capacity: 42000 | Range: 8000
        for v_id in range(1001, 1011):
            self._app_data.add_vehicle(Vehicle(v_id, "Scania", 42000, 8000))
            self._app_data.observe_vehicle_id(v_id)
            
        # 1011-1025: Man | Capacity: 37000 | Range: 10000
        for v_id in range(1011, 1026):
            self._app_data.add_vehicle(Vehicle(v_id, "Man", 37000, 10000))
            self._app_data.observe_vehicle_id(v_id)
            
        # 1026-1040: Actros | Capacity: 26000 | Range: 13000
        for v_id in range(1026, 1041):
            self._app_data.add_vehicle(Vehicle(v_id, "Actros", 26000, 13000))
            self._app_data.observe_vehicle_id(v_id)

    def _load_hubs_database(self):
        """Currently initialize hubs for every city on program startup"""
        # Added safety check in case self._app_data.hubs is a dict or list
        if self._app_data.hubs:
            return

        for c in City:
            self._app_data.add_hub(Hub(c))