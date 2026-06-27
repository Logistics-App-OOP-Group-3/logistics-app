from core.application_data import ApplicationData
from core.system_report import SystemReport
from core.command_factory import CommandFactory
from core.engine import Engine
from services.route_service import RouteService
from services.package_service import PackageService
from services.vehicle_service import VehicleService

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
