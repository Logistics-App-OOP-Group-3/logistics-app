import unittest
from core.application_data import ApplicationData
from services.package_service import PackageService
from services.route_service import RouteService
from services.vehicle_service import VehicleService
from models.route.route_stop import RouteStop
from enums.city import City
from models.vehicle import Vehicle
from models.hub import Hub

class TestLogisticsFlow(unittest.TestCase):
    def setUp(self):
        self.app_data = ApplicationData()
        self.package_service = PackageService(self.app_data)
        self.route_service = RouteService(self.app_data)
        self.vehicle_service = VehicleService(self.app_data)

    def test_full_package_delivery_flow(self):
        sydney_hub = Hub(City.SYD)
        melbourne_hub = Hub(City.MEL)
        self.app_data.add_hub(sydney_hub)
        self.app_data.add_hub(melbourne_hub)

        test_vehicle = Vehicle(1001, "testTruck", 1000.0, 10000.0)
        self.app_data.add_vehicle(test_vehicle)

        pkg = self.package_service.create_package(City.SYD, City.MEL, 40.0, "test@test.com")
        sydney_hub.add_single_package(pkg)
        self.assertEqual(pkg._package_id, 1)

        stops = [RouteStop(City.SYD), RouteStop(City.MEL)]
        route = self.route_service.create_route(stops)
        self.app_data.add_route(route)
        
        vehicle = self.vehicle_service.find_available_vehicle_for_distance(route.total_distance)
        
        self.route_service.assign_truck_to_route(route, vehicle)
        self.route_service.assign_packages_from_hubs(route, vehicle)
        
        self.assertEqual(pkg._route_id, route._route_id) 
        
        self.route_service.start_route(route)
        self.route_service.complete_all_routes_next_stop()
        
        self.assertEqual(pkg._status.name, "IN_TRANSIT")

if __name__ == '__main__':
    unittest.main()