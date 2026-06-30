from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.vehicle import Vehicle
    from core.application_data import ApplicationData
    
class VehicleService:
    """ Singleton class for serving business logic for vehicles"""

    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data
        
    #TODO We can add it later
    # def create_vehicle(self, params):
    #     #TODO: call app_data id gen
    #     ...
    
    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        return self._app_data.find_vehicle(vehicle_id)
    
    def get_all_vehicles(self) -> list[Vehicle]:
        return list(self._app_data.vehicles)
        
        
    def find_available_vehicle_for_distance(self, distance: int) -> Vehicle | None:
        """ Return: Vehicle -> available vehicle for this distance
                    None -> no vehicle can cover this distance right now """
        for vehicle in self._app_data.vehicles:
            if (vehicle.route_id is None
                and
                vehicle.max_range >= distance
                ):
                return vehicle
        
        return None