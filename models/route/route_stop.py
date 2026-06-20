from datetime import datetime

class RouteStop:
    
    ### Represents a single stop in a route.
    ### - location code (SYD)
    ### - expected arrival/departure time
    
    def __init__(self, location: str, expected_time: datetime):
        self.location = location
        self.time = expected_time
        
    def __str__(self):
        return f"{self.location} ({self.expected_time:%d/%m/%Y %H:%M})"
    
    
# Example Usage of routeStop

# stop = RouteStop(
#     "SYD",
#     datetime(2025, 10, 12, 6, 0)
# )

# print(stop)