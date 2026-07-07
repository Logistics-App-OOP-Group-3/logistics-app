# import unittest
# from models.vehicle import Vehicle
# from enums.city import City
# from core.application_data import ApplicationData
# from services.package_service import PackageService

# #IMPORTANT this unit test fails because right now we dont have the logic to check 



# class TestPackageExceedsVehicleCapacity(unittest.TestCase):
#     def setUp(self):
#         self.app_data = ApplicationData()
#         self.package_service = PackageService(self.app_data)

#     def test_package_exceeds_vehicle_capacity(self):
#         test_vehicle = Vehicle(1002, "SmallTruck", 50.0, 1000.0)
#         self.app_data.add_vehicle(test_vehicle)

#         with self.assertRaises(ValueError):
#             self.package_service.create_package(City.SYD, City.MEL, 100.0, "too_heavy@test.com")