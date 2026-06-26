from enums.city import City
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.route.route import Route
    from models.package.package import Package


class Vehicle:
    def __init__(self, vehicle_id: int, name: str, capacity: int, max_range: int):
        self._vehicle_id = vehicle_id
        self._name = name
        self._max_capacity = capacity
        self._max_range = max_range

        self._packages: dict[int, Package] = {}
        self._route: Route | None = None

    def add_packages(self, packages):
        """Packages arg can be single element list for single package"""
        for package in packages:
            self._packages[package.id] = package

    def remove_packages(self, city: City):
        to_remove = [p for p in self._packages.values() if p.end_location == city]
        
        for package_id in to_remove:
            self._packages.pop(package_id)

    @property  # calculated
    def remaining_capacity(self):
        return self._max_capacity - sum(
            package.weight for package in self._packages.values()
        )

    @property  # vehicle_id
    def vehicle_id(self):
        return self._vehicle_id

    @property  # name
    def name(self):
        return self._name

    @property  # capacity
    def capacity(self):
        return self._max_capacity

    @property  # max_range
    def max_range(self):
        return self._max_range

    @property  # route
    def route(self):
        return self._route

    def assign_route(self, route):
        self._route = route

    @classmethod
    def from_csv(cls, input_line: str):
        tokens = input_line.split(',')

        vehicle_id = int(tokens[0])
        name = tokens[1]
        capacity = int(tokens[2])
        max_range = int(tokens[3])

        return cls(vehicle_id, name, capacity, max_range)

    # Test implementation, not for Business logic
    def __str__(self):
        return (
            f"{self.vehicle_id}.{self.name} "
            f"MaxCapacity: {self.capacity} "
            f"MaxKMRange: {self.max_range}"
        )