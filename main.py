from core.application_data import ApplicationData
from core.system_report import SystemReport
from core.command_factory import CommandFactory
from core.engine import Engine
from services.route_service import RouteService
from services.package_service import PackageService

app_data = ApplicationData()
route_service = RouteService(app_data)
package_service = PackageService(app_data)
# system_report = SystemReport(app_data)
# print(system_report.info_vehicle_storage())
cmd_factory = CommandFactory(app_data)
engine = Engine()

engine.start()