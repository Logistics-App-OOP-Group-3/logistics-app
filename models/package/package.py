from enums.package_status import PackageStatus



class Package:
    
    def __init__(self, package_id: int, start_location: str, end_location: str, weight: float, contact_info: str):
        self.package_id = package_id
        
        self.start_location = start_location
        self.end_location = end_location
        
        self.weight = weight
        self.contact_info = contact_info
        
        self.route_id = None
        
        self.status = PackageStatus.NOT_ASSIGNED

    def assign_to_route(self, route_id: int):
        self.route_id = route_id
        self.status = PackageStatus.ASSIGNED
        
    def start_delivery(self):
        self.status = PackageStatus.IN_TRANSIT
        
    def mark_delivered(self):
        self.stats = PackageStatus.DELIVERED
        
    def __str__(self):
        return (
            f"Package {self.package_id}: "
            f"{self.start_location} -> {self.end_location} "
            f"({self.status.value})"
        )    