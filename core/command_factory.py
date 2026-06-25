
from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand


from typing import TYPE_CHECKING
# TYPE_CHECKING is bool var - used for importing for annotation purposes
# True: during code static parsing
# False: during program execution
if TYPE_CHECKING:
    from core.application_data import ApplicationData
    from services.route_service import RouteService
    from services.package_service import PackageService

class CommandFactory:
    def __init__(self, data: ApplicationData, route_service: RouteService, package_service: PackageService): #TODO: Add package service
        self._app_data = data
        self._route_service = route_service
        self._package_service = package_service
        
        
    def create(self, input_line:str):
        cmd, *params = input_line.split()
        
        cmd = cmd.lower()
        
        if cmd == "createpackage":
            return CreatePackageCommand(params, self._app_data, self._package_service, self._route_service)
        if cmd == "createroute":
            return CreateRouteCommand(params, self._app_data, self._route_service)
        if cmd == "":
            pass
        if cmd == "":
            pass
        if cmd == "":
            pass

        raise ValueError(f"Invalid command name: {cmd}!")
    