
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.vehicle import Vehicle
    from core.application_data import ApplicationData
    
class VehicleService:
    """ Singleton class for serving business logic for vehicles"""

    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data
        
    def available_vehicle_for_distance(self, distance: int) -> Vehicle | None:
        """ Return: Vehicle -> available vehicle for this distance
                    None -> no vehicle can cover this distance right now """
        for vehicle in self._app_data.vehicles:
            if (vehicle.route_id == None
                and
                vehicle.max_range <= distance
                ):
                return vehicle
        
        return None   