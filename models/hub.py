
from enums.city import City
from models.package import Package
from enums.package_status import PackageStatus

class Hub:
    """
        Holds packages for clients to leave(for now) #todo: and receive(for later).
        Each city represents one hub.
        For now City is UID for hubs.
    """
    
    def __init__(self, city: City):
        self._city = city
        self._packages: dict[int, Package] = dict()
        self._delivered_packages: dict[int, Package] = dict()
        self._packages_weight: int = 0

## PROPERTY   
    @property
    def city(self):
        return self._city
    @property
    def packages_ids(self):
        return tuple(self._packages.keys())
    @property
    def packages(self):
        return tuple(self._packages.values())
    @property
    def delivered_packages_ids(self):
        return tuple(self._delivered_packages.keys())
    @property
    def delivered_packages(self):
        return tuple(self._delivered_packages.values())
    @property
    def packages_weight(self):
        return self._packages_weight
    @property                                #calculated
    def package_count(self):
        return len(self._packages)

## PUBLIC METHODS
    def find_packages_for_locations(self, cities: list[City]) -> list[Package]:
        """Return unassigned packages whose end_location is in cities."""
        set_cities = set(cities)
        return [package
            for package in self._packages.values()
            if package.route_id is None and
            package.end_location in set_cities 
            ]
        
    def info_not_assigned_packages_by_end_location(self) -> str:
        """ Returns: 
                "end_location [total_packages_weight kg.] packages_count"
                    line for each package end_location in hub
        """
        
        end_location_packages = self._total_not_assigned_weight_by_end_location()
        
        result = [f"Packages in {self.city.value}:\n"]
        header = f"  {'END_LOCATION':^14}|{'WEIGHT':^16}|{"COUNT":^9}"
        
        result.append(header)
        result.append(2 * ' ' + (len(header) - 2) * '-')
        
        for end_location, data in end_location_packages.items():
            package_format = "package" if data[1] == 1 else "packages"
            line = f"  {end_location.value:.<13}: [{data[0]:^10.2f} kg.] {data[1]} {package_format}"
            result.append(line)

        result.append('')
        return '\n'.join(result)
                
                
    def add_single_package(self, package: Package, delivered: bool = False):
        """
            Adds package to the hub
                param[1]: delivered
                False: package left from client for delivery
                True: package left from delivery service
        """
        
        if delivered == True:
            if package.package_id in self._delivered_packages:
                raise ValueError(f"Adding delivered package to hub error: "
                                 f"Package {package.package_id} already in {self._city.value} hub!")

            self._delivered_packages[package.package_id] = package
        else: #delivered == False:
            if package.package_id in self._packages:
                 raise ValueError(f"Adding package to hub error: "
                                  f"Package {package.package_id} already in {self._city.value} hub!")
                 
            self._packages[package.package_id] = package
            self._packages_weight += package.weight
    
    def remove_single_package(self, package_id: int, from_delivered: bool = False):
        """
            Remove package from the hub.
                param[1]: from_delivered
                False: package taken out to be delivered
                True: client receiving already delivered package
        """
        
        target_dict = self._delivered_packages if from_delivered else self._packages

        if package_id not in target_dict:
            raise ValueError(f"Package {package_id} not found in {self._city.name}")

        package = target_dict.pop(package_id)
        if not from_delivered: 
            self._packages_weight -= package.weight
        return package
            
## PRIVATE METHODS

    def __str__(self):
        return (
            f"Hub: {self.city.name}"
            f" - Packages: {self.package_count}, Total_weigth: {self.packages_weight}"
            )
        
    def _total_not_assigned_weight_by_end_location(self) -> dict[City,tuple[int, int]]:
        """ Returns: total_weight and count of not-yet assigned packages
                at each package.end_location, sorted by descending total_weight """
        
        summaries = {}
        for package in self._packages.values():
            if package.status != PackageStatus.NOT_ASSIGNED:
                continue
            end_location = package.end_location
            total_weight, count  = summaries.get(end_location, (0, 0))
            summaries[end_location] = (total_weight + package.weight, count +1)
            
        return dict(
            sorted(summaries.items(), key = lambda item: item[1][0], reverse=True)
            )
            
        
        