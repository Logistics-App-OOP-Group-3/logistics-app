from enums.package_status import PackageStatus
from enums.city import City


class Package:
    
    def __init__(self, package_id: int, start_location: City, end_location: City, weight: float, contact_info: str):
        self._package_id = package_id
        self._start_location = start_location
        self._end_location = end_location
        
        self._weight = weight
        self._contact_info = contact_info
        
        self._route_id = None
        
        self.status = PackageStatus.NOT_ASSIGNED

## PROPERTIES
    @property
    def package_id(self):
        return self._package_id
    @property
    def start_location(self):
        return self._start_location
    @property
    def end_location(self):
        return self._end_location
    @property
    def weight(self):
        return self._weight
    @property
    def contact_info(self):
        return self._contact_info
    @contact_info.setter
    def contact_info(self, value: str):
        self._ensure_valid_contact_info(value)
        self._contact_info = value
    @property
    def route_id(self):
        return self._route_id
    @route_id.setter
    def route_id(self, value: int):
        self._ensure_valid_route_id(value)
        self._route_id = value

## PUBLIC METHODS
    def assign_to_route(self, route_id: int):
        self._route_id = route_id
        self.status = PackageStatus.ASSIGNED
        
    def start_delivery(self):
        self.status = PackageStatus.IN_TRANSIT
        
    def mark_delivered(self):
        self.status = PackageStatus.DELIVERED
    
    def short_info(self) -> str:
        return f"[{self._package_id}] {self._start_location.value} -> {self._end_location.value}"
        
    def __str__(self):
        return (
            f"Package {self.package_id}: "
            f"{self.start_location} -> {self.end_location} "
            f"({self.status.value})"
        )    
        
## VALIDATION METHODS    
    def _ensure_valid_contact_info(value: str):
        if not value:
            raise ValueError("Package contact info cannot be empty!")
        if not 5 <= len(value) <= 100:
            raise ValueError("Illegal package contact info length [5:100]")
    
    def _ensure_valid_route_id(value: int):
        if not value:
            raise ValueError("Package route id cannot be None!")