from core.application_data import ApplicationData
from core.system_report import SystemReport
from core.command_factory import CommandFactory
from core.engine import Engine
from services.route_service import RouteService
from services.package_service import PackageService

# app_data = ApplicationData()
# route_service = RouteService(app_data)
# package_service = PackageService(app_data)
# # system_report = SystemReport(app_data)
# # print(system_report.info_vehicle_storage())
# cmd_factory = CommandFactory(app_data, route_service, package_service)
# engine = Engine(cmd_factory)

# engine.start()


from models.route.city_graph import CityGraph as cg
from enums.city import City as c
from models.route.route import Route
from models.route.route_stop import RouteStop


a = [c.BRI, c.SYD, c.MEL, c.ADL, c.ASP, c.DAR, c.PER]
tot_distance = 0
for i in range(len(a) - 1):
    tot_distance += cg.distance(a[i], a[i+1])
    print(i)
    
print(tot_distance)