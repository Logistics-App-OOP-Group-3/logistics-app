from commands.base.base_command import BaseCommand
import commands.validation_helper as val_help
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.package_service import PackageService
    from services.route_service import RouteService
    from core.application_data import ApplicationData

class CreatePackageCommand(BaseCommand):
    """
    input_trigger: createpackage
        param[0]: enum.City
        param[1]: enum.City
        param[2]: float
        param[3]: string
    exectuion:
        CreatePackage with:
            start_location: param[0]
            end_location:   param[1]
            weight:         param[2]
            contact_info:   param[3]
        AddToHub by matching start_location
        Display available routes(capacity check not included)
    """
    
    def __init__(self, params, app_data: 'ApplicationData', package_service: 'PackageService', route_service: 'RouteService'):
        val_help.validate_params_count(params, 4, "CreatePackageCommand")
        super().__init__(params, app_data)
        self._package_service = package_service
        self._route_service = route_service
    
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
        
        # Основно съобщение за успех
        result = [f"\nPackage {package.package_id} created successfully and left at hub {hub.city.value}."]
        
        # Търсим налични маршрути за пакета
        available_routes = self._route_service.find_routes_for_package(package)
        
        if not available_routes:
            result.append("No available routes currently found for this package's destination.\n")
        else:
            result.append("Available routes for assignment:")
            for route in available_routes:
                result.append(f"--- Route #{route.route_id} ---")
                # Използваме route_stops_info() вместо __str__, за да видим капацитета по спирки
                vehicle = self.app_data.find_vehicle(route.vehicle_id)
                result.append(route.route_stops_info(vehicle.max_capacity))
                result.append("-" * 25)
            result.append("")
        
        return "\n".join(result)