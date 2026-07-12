from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count, try_parse_int
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.route_service import RouteService
    from core.application_data import ApplicationData

class AssignPackageCommand(BaseCommand):
    """
    input_trigger: assignpackage
        param[0]: package_id: int
        param[1]: route_id: int
    execution:
        Assigns package to route after route location validation
        and vehicle weight capacity validation
    """
    def __init__(self, params, app_data: 'ApplicationData', route_service: 'RouteService'):
        #<package_id> <route_id>
        validate_params_count(params, 2, "AssignPackageCommand")
        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):
        
        package_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])
        
        package = self._app_data.find_package(package_id)
        
        if route_id == 0:
            return f"Package {package_id} remains at hub {package.start_location.value}."
        
        self._route_service.assign_package_to_route(package, route_id)
        
        return f"Package {package_id} assigned to route {route_id} successfully."