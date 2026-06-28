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



app_data = ApplicationData()
route_service = RouteService(app_data)
package_service = PackageService(app_data)
vehicle_service = VehicleService(app_data)
# system_report = SystemReport(app_data)
# print(system_report.info_vehicle_storage())

#TODO: ?? Command orchestrator approach. Instead of hiding everything in one service method, requiring different services coupling. ??
cmd_factory = CommandFactory(app_data, route_service, package_service, vehicle_service)
engine = Engine(cmd_factory)
engine.start()

# from models.package.package import Package
# from enums.city import City 

# p1 = Package(1, City.MEL, City.ADL, 100, "Bat mincho izvestniq")
# p2 = Package(2, City.MEL, City.ADL, 100, "Bat mincho izvestniq")

# app_data = ApplicationData()

# app_data.hubs[0].add_multiple_packages([p1,p2])
# for h in app_data.hubs:
#     print(h)




