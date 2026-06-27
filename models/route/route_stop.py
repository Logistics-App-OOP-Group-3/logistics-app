from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from enums.city import City

class RouteStop:
    
    ### Represents a single stop in a route.
    ### - location code (SYD)
    ### - expected arrival/departure time
    
    def __init__(self, location: City):
        self.location = location

        self.arrival_time: datetime | None = None
        self.departure_time: datetime | None = None
        self._available_capacity = 0

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