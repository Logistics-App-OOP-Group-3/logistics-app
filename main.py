from core.application_data import ApplicationData
# from core.system_report import SystemReport
from core.command_factory import CommandFactory
from core.engine import Engine
from services.route_service import RouteService
from services.package_service import PackageService
from services.vehicle_service import VehicleService

"""
    Use case 5:  package_expected_arival time & location
        route- stop expected time, last_completed stop
    Use case 4: list_packages, by route_id | status + location
    Use case 3: all delivery roots (for now no pending routes for vehicle) 
                delivery weigth - load & unload at each stop 
                                  arrival_time
    Use case2: load packages from hubs 
    Use case1: create package, list routes, choose route or leave at hub
"""

"""
assign_truck_to_route_command.py is currently not usable:
    Since we dont create routes without trucks (for now)


create_package_command.py handles assigning of package


create_route_command.py should have 2 version
    1: where packets get loaded from hubs automatically (current implementation)
    2: where route is simply created as a logical followup of Use Case 4. 
    (to add rotting unassigned packages)
"""

app_data = ApplicationData()
#! Services singletons created in command factory
cmd_factory = CommandFactory(app_data)
engine = Engine(cmd_factory)
engine.start()





