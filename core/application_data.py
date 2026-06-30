from __future__ import annotations

from typing import TYPE_CHECKING

from models.vehicle import Vehicle
from models.hub import Hub
from enums.city import City

if TYPE_CHECKING:
    from models.route.route import Route
    from models.package.package import Package


class ApplicationData:
    """
    Central in-memory storage for all domain objects.
    Responsible for ID generation + object registration.
    """

    def __init__(self):
        self._id_package = 0
        self._id_route = 0
        self._id_vehicle = 0

        self._packages: dict[int, Package] = dict()
        self._routes: dict[int, Route] = dict()
        self._vehicles: dict[int, Vehicle] = dict()
        self._hubs: dict[City, Hub] = dict()

    # Read Only Access

    @property
    def packages(self) -> dict[int, Package]:
        return self._packages

    @property
    def routes(self) -> dict[int, Route]:
        return self._routes

    @property
    def vehicles(self) -> tuple[Vehicle, ...]:
        return tuple(self._vehicles.values())

    @property
    def vehicle_map(self) -> dict[int, Vehicle]:
        return self._vehicles.copy()

    @property
    def hubs(self) -> tuple[Hub, ...]:
        return tuple(self._hubs.values())

    # Generating ID's

    def generate_package_id(self) -> int:
        self._id_package += 1
        return self._id_package

    def generate_route_id(self) -> int:
        self._id_route += 1
        return self._id_route

    def generate_vehicle_id(self) -> int:
        self._id_vehicle += 1
        return self._id_vehicle
    

    # Changed sync ids to refresh ids this makes it so we dont need a max_id varaible and also we can call the method without parameters
    def refresh_ids(self) -> None:

        #Called  after loading from file to prevent id collisions
        self._id_package = max(self._packages.keys(), default=0)
        self._id_route = max(self._routes.keys(), default=0)
        self._id_vehicle = max(self._vehicles.keys(), default=0)
    

    # Find methods
    def find_package(self, id: int) -> Package:
        if id not in self._packages:
            raise ValueError(f"Package id {id} not found")
        return self._packages[id]

    def find_route(self, id: int) -> Route:
        if id not in self._routes:
            raise ValueError(f"Route id {id} not found")
        return self._routes[id]

    def find_vehicle(self, id: int) -> Vehicle:
        if id not in self._vehicles:
            raise ValueError(f"Vehicle id {id} not found")
        return self._vehicles[id]

    def find_hub(self, city: City) -> Hub:
        if city not in self._hubs:
            raise ValueError(f"Hub {city.value} not found")
        return self._hubs[city]

    # Add methods

    def add_route(self, route: Route) -> None:
        self._routes[route.route_id] = route

    def add_package(self, package: Package) -> None:
        self._packages[package.package_id] = package

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.vehicle_id] = vehicle

    def add_hub(self, hub: Hub) -> None:
        self._hubs[hub.city] = hub