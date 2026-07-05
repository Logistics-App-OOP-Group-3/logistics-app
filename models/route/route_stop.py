from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from enums.city import City
    from enums.route_status import RouteStatus
    from models.package.package import Package

class RouteStop:
    
    ### Represents a single stop in a route.
    ### - location code (SYD)
    ### - expected arrival/departure time
    
    def __init__(self, location: City):
        self._location = location

        self.arrival_time: datetime | None = None
        self.departure_time: datetime | None = None
        
        self._pick_up_weigth = 0
        self._drop_off_weigth = 0
        
        self._stop_status = RouteStatus.PLANNED
    
    @property
    def location(self):
        return self._location
    
    @property
    def pick_up_weigth(self):
        return self._pick_up_weigth
    @property
    def drop_off_weigth(self):
        return self._drop_off_weigth
    @property
    def stop_status(self):
        return self._stop_status
    @stop_status
    def stop_status(self, value: RouteStatus):
        self._stop_status = value
    
    def add_pick_up_weigth(self, value: int):
        self._pick_up_weigth += value
    def add_drop_off_weigth(self, value: int):
        self._drop_off_weigth += value

    def __str__(self):
        return (
            f"{self.location.name} "
            f"[arr: {self.arrival_time:%d/%m/%Y %H:%M} | "
            f"dep: {self.departure_time:%d/%m/%Y %H:%M}]"
            if self.arrival_time and self.departure_time
            else f"{self.location.name} (time not calculated)"
        )
    
# Example Usage of routeStop

# stop = RouteStop(
#     "SYD",
#     datetime(2025, 10, 12, 6, 0)
# )

# print(stop)