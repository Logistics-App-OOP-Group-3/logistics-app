from core.application_data import ApplicationData
from core.system_report import SystemReport
from core.command_factory import CommandFactory
from core.engine import Engine
from models.route.route_service import RouteService

app_data = ApplicationData()
for vehicle in app_data._vehicles.values():
    print(vehicle)
route_service = RouteService(app_data)
# system_report = SystemReport(app_data)
# print(system_report.info_vehicle_storage())
# cmd_factory = CommandFactory(app_data)
# engine = Engine()

# engine.start()