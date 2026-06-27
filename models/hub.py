
from enums.city import City
from models.package.package import Package

class Hub:
    """
        Holds packages for clients to leave(for now) #TODO: and receive(for later).
        Each city represents one hub.
        For now City is UID for hubs.
    """
    
    def __init__(self, city: City):
        self._city = city
        self._packages: dict[int, Package] = dict() #TODO: posible workaround to hold only ids without Package objects
        self._packages_weigth: int = 0

## PROPERTY   
    @property
    def city(self):
        return self._city
    @property
    def packages_ids(self):
        return tuple(self._packages.keys())
    @property
    def packages_weigth(self):
        return self._packages_weigth
    @property                                #calculated
    def package_count(self):
        return len(self._packages)

## PUBLIC METHODS   
    def add_single_package(self, package: Package):
        if package.package_id not in self._packages: 
            self._packages[package.package_id] = package
            self._packages_weigth += package.weight
            
    def add_multiple_packages(self, packages: list[Package]):
        for package in packages:
            self.add_single_package(package)
    
    def remove_single_package(self, package: Package):
        if package.package_id not in self._packages:
            raise ValueError(f"Package not in hub {self.city.name}")
        self._packages.pop(package.package_id)
        self._packages_weigth -= package.weight
        
    def remove_multiple_packages(self, packages_ids):
        for package_id in packages_ids:
            self.remove_single_package(package_id)
            
## PRIVATE METHODS

    def __str__(self):
        return (
            f"Hub: {self.city.name}"
            f" - Packages: {self.package_count}, Total_weigth: {self.packages_weigth}"
            )