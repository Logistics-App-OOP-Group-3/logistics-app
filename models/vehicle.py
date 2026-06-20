from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.route.route import Route

class Vehicle:
    
    vehicles_csv_line = [
        "1001-1010,Scania,42_000,8_000,",
        "1011-1025,Man,37_000,10_000",
        "1026-1040,Actros,26_000,13_000"
    ]
    
    def __init__(self, id:int, name: str, capacity: int, max_range: int):
        self._id = id
        self._name = name
        self._max_capacity = capacity
        self._max_range = max_range     # kilometers
        self._packages: dict[int, object] = {} #TODO: object -> Package
        self._route: Route = None
  
    
    def add_packages(self, packages):
        """Packages arg can be single element list for single package"""
        for package in packages:
            self._packages[package.id] = package
    
    def remove_packages(self, city:str): #TODO: str -> ENUM
        """Remove packages based on the city arg == package.end_location"""
        for package in self._packages.values():
            if package.city == city:
                self._packages.pop(package.id)
                
    @property             # calculated
    def remaining_capacity(self):
        return self._max_capacity - sum([package.weight for package in self._packages])
    @property             # id
    def id(self):
        return self._id
    @property             # name
    def name(self):
        return self._name
    @property             # capacity
    def capacity(self):
        return self._max_capacity  
    @property             # max_range
    def max_range(self):
        return self._max_range
        
    @classmethod
    def from_csv(cls, input_line: str = None) -> Vehicle:
        tokens = input_line.split(',')
        id = int(tokens[0])
        name = tokens[1]
        capacity = int(tokens[2])
        max_range = int(tokens[3])
        
        return cls(id, name, capacity, max_range)
    
    # Test implementation, not for Busines logic
    def __str__(self):
        return f"{self._id}.{self.name} MaxCapacity: {self.capacity} MaxKMRange:{self.max_range}"