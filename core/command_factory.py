
from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.package_info_command import PackageInfoCommand
from commands.route_info_command import RouteInfoCommand
from services.route_service import RouteService
from services.package_service import PackageService
from services.vehicle_service import VehicleService
from core.data_repository import DataRepository


from typing import TYPE_CHECKING
# TYPE_CHECKING is bool var - used for importing for annotation purposes
# True: during code static parsing
# False: during program execution
if TYPE_CHECKING:
    from core.application_data import ApplicationData

class CommandFactory:
    def __init__(self, app_data: ApplicationData):
    
        self._app_data = app_data
        self._route_service = RouteService(app_data)
        self._package_service = PackageService(app_data)
        self._vehicle_service = VehicleService(app_data)
        self._data_repository = DataRepository(app_data)
        self._data_repository.load()
        
    def create(self, input_line:str):
        cmd, *params = input_line.split()
        
        cmd = cmd.lower()
        
        if cmd == "createpackage":
            return CreatePackageCommand(params, self._app_data, self._package_service, self._route_service)
        if cmd == "createroute":
            return CreateRouteCommand(params, self._app_data, self._route_service, self._vehicle_service)
        if cmd == "packageinfo":
            return PackageInfoCommand(params, self._app_data, self._package_service, self._route_service)
        if cmd == "routeinfo":
            return RouteInfoCommand(params,self._app_data, self._route_service)
        if cmd == "":
            pass

        raise ValueError(f"Invalid command name: {cmd}!")
    