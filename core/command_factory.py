
from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.package_info_command import PackageInfoCommand


from typing import TYPE_CHECKING
# TYPE_CHECKING is bool var - used for importing for annotation purposes
# True: during code static parsing
# False: during program execution
if TYPE_CHECKING:
    from core.application_data import ApplicationData
    from services.route_service import RouteService
    from services.package_service import PackageService
    from services.vehicle_service import VehicleService

class CommandFactory:
    def __init__(self,
                 app_data: ApplicationData,
                 route_service: RouteService,
                 package_service: PackageService,
                 vehicle_service: VehicleService): 
        
        self._app_data = app_data
        self._route_service = route_service
        self._package_service = package_service
        self._vehicle_service = vehicle_service
        
        
    def create(self, input_line:str):
        cmd, *params = input_line.split()
        
        cmd = cmd.lower()
        
        if cmd == "createpackage":
            return CreatePackageCommand(params, self._app_data, self._package_service, self._route_service)
        if cmd == "createroute":
            return CreateRouteCommand(params, self._app_data, self._route_service, self._vehicle_service)
        if cmd == "packageinfo":
            return PackageInfoCommand(params, self._app_data, self._package_service, self._route_service)
        if cmd == "":
            pass
        if cmd == "":
            pass

        raise ValueError(f"Invalid command name: {cmd}!")
    