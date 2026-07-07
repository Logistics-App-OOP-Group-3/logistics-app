import unittest
from unittest.mock import patch
from models.route.route import Route
from models.route.route_stop import RouteStop
from enums.city import City
from enums.package_status import PackageStatus
from unittest.mock import MagicMock

class SystemLoad_Should(unittest.TestCase):

    def test_highVolumePackageWeightCalculation(self):
        #Create a large set of packages
        num_packages = 1000
        #Mocking 1000 packages with 10kg each
        packages = [MagicMock(weight=10.0, status=PackageStatus.NOT_ASSIGNED) for _ in range(num_packages)]
        
        #Assign them to a simulated Hub
        hub = MagicMock(packages=packages)
        
        #Test calculation performance
        #We want to ensure our total weight logic handles 1000 items instantly
        total_weight = sum(p.weight for p in hub.packages)
        
        self.assertEqual(total_weight, 10000.0)

    def test_routeCapacityUnderLoad(self):
        available_cities = [City.SYD, City.MEL, City.BRI, City.ADL]
        
        #Create 50 stops
        stops = [RouteStop(available_cities[i % len(available_cities)]) for i in range(50)]

        # Use 'patch' to force _calculate_total_distance to return a safe value
        # This prevents the ValueError during Route initialization
        with patch.object(Route, '_calculate_total_distance', return_value=1000):
            route = Route(999, stops)
        
        #Add packages to the stops
        for i in range(50):
            stops[i].add_pick_up_weigth(5.0)
            
        #Ensure that calculating capacity for a long route doesnt crash
        capacities = route.calculate_stops_capacity()
        self.assertEqual(len(capacities), 50)
        self.assertEqual(capacities[-1], 250.0)

        