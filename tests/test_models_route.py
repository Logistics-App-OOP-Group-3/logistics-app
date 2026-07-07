import unittest
from datetime import datetime, timedelta
from models.route.route import Route
from models.route.route_stop import RouteStop
from enums.city import City
from enums.route_status import RouteStatus

class Route_Should(unittest.TestCase):
    def setUp(self):
        # We define two stops because a route requires at least two
        self.stops = [RouteStop(City.SYD), RouteStop(City.MEL)]
        self.start_time = datetime(2026, 10, 22, 10, 0)
        self.route = Route(1, self.stops, self.start_time)

    def test_initializer_AssignsAllPropertiesCorrectly(self):
        self.assertEqual(self.route.route_id, 1)
        self.assertEqual(len(self.route.stops), 2)
        self.assertEqual(self.route.status, RouteStatus.PLANNED)

    def test_initializer_RaisesError_WhenRouteHasFewerThanTwoStops(self):
        with self.assertRaises(ValueError):
            Route(2, [RouteStop(City.SYD)])

    def test_addPackage_UpdatesPackageListSuccessfully(self):
        self.route.add_package(999)
        self.assertIn(999, self.route.packages_ids)

    def test_addPackage_PreventsAddingTheSamePackageTwice(self):
        self.route.add_package(999)
        with self.assertRaises(ValueError):
            self.route.add_package(999)

    def test_weightAtStop_CalculatesLoadCorrectly(self):
        # Picking up 100 in Sydney, dropping off 50 in Melbourne
        self.stops[0].add_pick_up_weigth(100.0)
        self.stops[1].add_drop_off_weigth(50.0)
        
        self.assertEqual(self.route.weight_at_stop(0), 100.0)
        self.assertEqual(self.route.weight_at_stop(1), 50.0)

    def test_canDeliverBetween_ValidatesAllowedDirection(self):
        # You can move from Start to End, but not backward
        self.assertTrue(self.route.can_deliver_between(City.SYD, City.MEL))
        self.assertFalse(self.route.can_deliver_between(City.MEL, City.SYD))

    def test_totalDistance_IsGreaterZero(self):
        self.assertGreater(self.route.total_distance, 0)

    def test_arrivalTime_MatchesThePlannedStartTime(self):
        self.assertEqual(self.route.stops[0].arrival_time, self.start_time)

    def test_nextIncompletedStop_ReturnsCorrectIndex(self):
        self.assertEqual(self.route.get_index_of_next_incompleted_stop(), 0)
        
        self.stops[0].stop_status = RouteStatus.COMPLETED
        self.stops[1].stop_status = RouteStatus.IN_PROGRESS
        
        self.assertEqual(self.route.get_index_of_next_incompleted_stop(), 1)

    def test_currentLocation_ReturnsNone_IfNoStopsFinished(self):
        self.assertIsNone(self.route.current_location)

    def test_calculateStopsCapacity_ShowsCorrectWeightAtEachStop(self):
        self.stops[0].add_pick_up_weigth(100.0)
        self.stops[1].add_drop_off_weigth(50.0)
        
        capacities = self.route.calculate_stops_capacity()
        self.assertEqual(capacities, [100.0, 50.0])

    def test_routeStopsInfo_CalculatesFreeCapacity(self):
        # Truck cap 500, load 100 Free 400
        self.stops[0].add_pick_up_weigth(100.0)
        info = self.route.route_stops_info(vehicle_max_capacity=500)
        
        self.assertIn("Free: [400.0 kg]", info)

    def test_get_current_stop_ReturnsCorrectStop(self):
        # Verify it identifies the stop based on arrival time
        check_time = self.start_time + timedelta(hours=2)
        current = self.route.get_current_stop(check_time)
        self.assertEqual(current.location, City.SYD)

    def test_strMethod_ContainsBasicInfo(self):
        output = str(self.route)
        self.assertIn("Route 1", output)
        self.assertIn("Status: Planned", output)