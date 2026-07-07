import unittest
from datetime import datetime, timedelta
from models.route.route import Route
from models.route.route_stop import RouteStop
from enums.city import City
from enums.route_status import RouteStatus


class TestRouteModel(unittest.TestCase):
    def setUp(self):
        # we define minimal testing stops route needs atleast 2 
        self.stops = [RouteStop(City.SYD), RouteStop(City.MEL)]
        self.start_time = datetime(2026, 10, 22, 10, 0)
        self.route = Route(1, self.stops, self.start_time)

    def test_route_initializer(self):
        self.assertEqual(self.route.route_id, 1)
        self.assertEqual(len(self.route.stops), 2)
        self.assertEqual(self.route.status, RouteStatus.PLANNED)
    
    def test_invalid_route_stops(self):
        with self.assertRaises(ValueError):
            Route(2, [RouteStop(City.SYD)])
    
    def test_weight_at_stop(self):
        self.stops[0].add_pick_up_weigth(100.0)
        self.assertEqual(self.route.weight_at_stop(0), 100.0)
    
    def test_can_deliver_between(self):
        self.assertTrue(self.route.can_deliver_between(City.SYD, City.MEL))
        self.assertFalse(self.route.can_deliver_between(City.MEL, City.SYD))

    def test_total_distance_calculation(self):
        self,self.assertGreater(self.route.total_distance, 0)

    def test_start_time_eta_influence(self):
        self.assertEqual(self.route.stops[0].arrival_time, self.start_time)

    def test_add_package_success(self):
        self.route.add_package(999)
        self.assertIn(999, self.route.packages_ids)
    def test_add_duplicate_package(self):
        self.route.add_package(999)
        with self.assertRaises(ValueError):
            self.route.add_package(999)