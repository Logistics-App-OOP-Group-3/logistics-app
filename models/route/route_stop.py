from datetime import datetime

class RouteStop:
    
    ### Represents a single stop in a route.
    ### - location code (SYD)
    ### - expected arrival/departure time
    
    def __init__(self, location: str):
        self.location = location

        self.arrival_time: datetime | None = None
        self.departure_time: datetime | None = None

    def __str__(self):
        return (
            f"{self.location} "
            f"(arr: {self.arrival_time:%d/%m/%Y %H:%M} | "
            f"dep: {self.departure_time:%d/%m/%Y %H:%M})"
            if self.arrival_time and self.departure_time
            else f"{self.location} (time not calculated)"
        )
    
# Example Usage of routeStop

# stop = RouteStop(
#     "SYD",
#     datetime(2025, 10, 12, 6, 0)
# )

# print(stop)