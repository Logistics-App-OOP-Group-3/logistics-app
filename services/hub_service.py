from typing import TYPE_CHECKING
from enums.package_status import PackageStatus

if TYPE_CHECKING:
    from enums.city import City
    from core.application_data import ApplicationData



class HubService:
    """ Singleton class for serving business logic for hubs"""
    
    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data
    

    
    def info_unassigned_packages_by_city(self) -> str:
        """ Return: 
                "city [total_packages_weight kg.] packages_count" 
                    line for each hub in app_data 
        """
        
        city_packages = self._total_not_assigned_weight_by_city()
        
        result = ['']
        header = f"  {'HUB':^14}|{'WEIGHT':^16}|{'COUNT':^9} "
        
        result.append(header)
        result.append(2 * ' ' + (len(header) - 2) * '-')
        for city, data in city_packages.items():
            package_format = "package" if data[1] == 1 else "packages"
            line = f"  {city.value:.<13}: [{data[0]:^10.2f} kg.] {data[1]} {package_format}"
            result.append(line)

        result.append('')
        return '\n'.join(result)
        
    
    def _total_not_assigned_weight_by_city(self) -> dict[City, tuple[int, int]]:
        """ Return: total_weight and count of not-yet-assigned packages
                    at each hub, sorted by descending total_weight """
                    
        summaries = {}
        for hub in self._app_data.hubs:
            not_assigned = [p for p in hub.packages if p.status == PackageStatus.NOT_ASSIGNED]
            summaries[hub.city] = (
                sum(p.weight for p in not_assigned),
                len(not_assigned)
            )
            
        return dict(
            sorted(summaries.items(), key=lambda item: item[1][0], reverse=True)
        )
