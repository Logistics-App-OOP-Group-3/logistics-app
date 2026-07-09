from commands.base.base_command import BaseCommand
import commands.validation_helper as val_help
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.package_service import PackageService
    from core.application_data import ApplicationData

class CreatePackageCommand(BaseCommand):
    def __init__(self, params, app_data: 'ApplicationData', package_service: 'PackageService'):
        val_help.validate_params_count(params, 4, "CreatePackageCommand")
        super().__init__(params, app_data)
        self._package_service = package_service
    
    def execute(self):
        start_location = val_help.try_parse_city(self.params[0])
        end_location = val_help.try_parse_city(self.params[1])
        weight = val_help.try_parse_float(self.params[2])
        contact_info = self.params[3]
        
        # Създаваме пакета чрез сървиза
        package = self._package_service.create_package(
            start_location, end_location, weight, contact_info
        )
        
        # Добавяме го в хъба
        hub = self._app_data.find_hub(start_location)
        hub.add_single_package(package)
        
        return f"Package {package.package_id} created successfully and left at hub {hub.city.value}."
    
        #TODO: Call find_routes_for_package and display the info
        #TODO: Call route_stops_info instead of __str__ to display available capacity per stop(refactor if needed)
        #TODO:  for the employee to look up and try to assign the package which if it cant fit will raise error
          