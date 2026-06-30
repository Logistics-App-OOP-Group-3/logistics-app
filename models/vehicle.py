from __future__ import annotations
from enums.city import City


class Vehicle:
    #TODO: Add current location in init params
    def __init__(self, vehicle_id: int, name: str, capacity: int, max_range: int):
        self._vehicle_id = vehicle_id
        self._name = name
        self._max_capacity = capacity
        self._max_range = max_range
        self._route_id: int | None = None
        # self._current_location: City = city_location

    @property                       # vehicle_id
    def vehicle_id(self):
        return self._vehicle_id
    @property                       # name
    def name(self):
        return self._name
    @property                       # capacity
    def max_capacity(self):
        return self._max_capacity
    @property                       # max_range
    def max_range(self):
        return self._max_range
    @property                       # route_id
    def route_id(self):
        return self._route_id
    @route_id.setter                # route_id
    def route_id(self, value: int):
        self._route_id = value
    # @property                       # current_location
    # def current_location(self):
    #     return self._current_location
    # @current_location.setter
    # def current_location(self, value: City):
    #     self._current_location = value


    # Test implementation, not for Business logic
    def __str__(self):
        return (
            f"{self.vehicle_id}.{self.name} "
            f"MaxCapacity: {self.max_capacity} "
            f"MaxKMRange: {self.max_range}"
        )
        
    @classmethod
    def from_csv(cls, input_line: str) -> Vehicle:
        """ Create vehicle from csv line """
        tokens = input_line.split(',')

        vehicle_id = int(tokens[0])
        name = tokens[1]
        capacity = int(tokens[2])
        max_range = int(tokens[3])

        return cls(vehicle_id, name, capacity, max_range)
    
    def to_csv(self) -> str:
        """ Serialize vehicle to csv format """
        return f'{self._vehicle_id},{self._name},{self._max_capacity},{self._max_range}'