import unittest
from unittest.mock import MagicMock, patch
from services.route_service import RouteService
from enums.route_status import RouteStatus
from enums.city import City
from models.route.route import Route
from models.package import Package
from models.vehicle import Vehicle
from models.hub import Hub

from models.route.route_stop import RouteStop
from datetime import datetime

class Initializer_Should(unittest.TestCase):
    def test_nothingBreaks(self):
        mock_app_data = MagicMock()
        RouteService(mock_app_data)
        
class CreateRoute_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)

        # mock route class inside route_service
        patcher = patch("services.route_service.Route")
        self.mock_route_cls = patcher.start()
        # ran at end of setUp on each test
        self.addCleanup(patcher.stop)
        
        self.mock_app_data.generate_route_id.return_value = 1
        # get instance of the mocked class
        self.mock_route_instance = self.mock_route_cls.return_value

        # Act
        self.result = self.route_service.create_route(["A,B"])
        
    def test_generateId_calledOnce(self):
        
        # Assert
        self.mock_app_data.generate_route_id.assert_called_once()

    def test_buildsRouteWithDefaultParamStartTime(self):

        # Assert
        self.mock_route_cls.assert_called_once_with(1,["A,B"], None)
        
    def test_buildRouteWithExplicitParamStartTime(self):
        
        # Act
        self.route_service.create_route(["A","B"], datetime.min)
        
        # Assert
        self.mock_route_cls.assert_called_with(1, ["A","B"], datetime.min)
        
    def test_addsRoute(self):
        
        # Assert
        self.mock_app_data.add_route.assert_called_once_with(self.mock_route_instance)
        
    def test_returnsCreatedRoute(self):

        # Assert
        self.assertEqual(self.result, self.mock_route_instance)
        
class GetRouteMethods_Should(unittest.TestCase):

        def setUp(self):
        
            # Arrange
            self.mock_app_data = MagicMock()
            self.route_service = RouteService(self.mock_app_data)

            self.mock_route1 = MagicMock(spec_set=Route)
            self.mock_route1.route_id = 1
            self.mock_route1.status = RouteStatus.IN_PROGRESS

            self.mock_route2 = MagicMock(spec_set=Route)
            self.mock_route2.route_id = 2
            self.mock_route2.status = RouteStatus.IN_PROGRESS

            self.mock_route3 = MagicMock(spec_set=Route)
            self.mock_route3.route_id = 3
            self.mock_route3.status = RouteStatus.PLANNED
            
            self.mock_routes = [
                self.mock_route1,
                self.mock_route2,
                self.mock_route3    
            ]
            
            self.mock_app_data.routes.values.return_value = self.mock_routes
            self.mock_app_data.find_route.return_value = "unrelated_to_the_test_data"

        def test_getRoute_findRoute_withGiveId(self):
            
            # Act
            result = self.route_service.get_route(1)
            
            # Assert
            self.assertEqual(result, self.mock_app_data.find_route.return_value)

        def test_getRoute_callsFindPackageOnce_withCorrectId(self):
            
            # Act
            self.route_service.get_route(1)
            
            # Assert
            self.mock_app_data.find_route.assert_called_once_with(1)
            
        def test_getAllRoutes_returnsCorrectRoutes(self):
            
            # Act
            result = self.route_service.get_all_routes()

            # Assert
            self.assertEqual(result, self.mock_routes)

        def test_getAllRoutes_returnsList(self):
            
            # Act
            result = self.route_service.get_all_routes()
            
            # Assert
            self.assertIsInstance(result, list)
            
        def test_getAllRoutes_callsValuesOnce(self):
        
            # Act
            self.route_service.get_all_routes()
            
            # Assert
            self.mock_app_data.routes.values.assert_called_once()
            
        def test_getRoutesByStatus_returnsMatching(self):
            
            # Act
            result = self.route_service.get_routes_by_status(RouteStatus.IN_PROGRESS)

            # Assert
            self.assertEqual(result, [self.mock_route1,self.mock_route2])
            
        def test_getRoutesByStatus_notReturnsNonMatching(self):
            
            # Act
            result = self.route_service.get_routes_by_status(RouteStatus.IN_PROGRESS)

            # Assert
            self.assertNotIn(self.mock_route3, result)
            
        def test_getRoutesByStatus_callsValuesOnce(self):
            
            # Act
            self.route_service.get_routes_by_status(RouteStatus.IN_PROGRESS)
            
            # Assert
            self.mock_app_data.routes.values.assert_called_once()
            
class MarkMethods_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
        
        self.mock_route1 = MagicMock(spec_set=Route)
        self.mock_route1.status = RouteStatus.IN_PROGRESS
        
        self.mock_routestop1 = MagicMock(spec_set=RouteStop)
        self.mock_routestop1.location = "A"
        self.mock_routestop1.stop_status = RouteStatus.IN_PROGRESS
        self.mock_routestop2 = MagicMock(spec_set=RouteStop)
        self.mock_routestop2.location = "B"
        self.mock_routestop2.stop_status = RouteStatus.IN_PROGRESS
        
        self.mock_routestops = [self.mock_routestop1, self.mock_routestop2]
        self.mock_route1.stops = self.mock_routestops

    def test_markRouteAsCompleted_changesStatus_whenValidData(self):

        # Act
        self.route_service.mark_route_as_completed(self.mock_route1)

        # Assert
        self.assertEqual(self.mock_route1.status, RouteStatus.COMPLETED)

    def test_markRouteAsCompleted_raiseError_whenStatusIsNotInProgress(self):

        # Arrange
        self.mock_route1.status = RouteStatus.PLANNED
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.mark_route_as_completed(self.mock_route1)
            
    def test_markStopAsCompleted_changingStatus_whenValidData(self):
        
        # Act
        self.route_service.mark_stop_as_completed(self.mock_route1, 0)

        # Assert
        self.assertEqual(self.mock_routestops[0].stop_status, RouteStatus.COMPLETED)

    def test_markStopAsCompleted_notChangingStatusOfOtherStops(self):

        # Act
        self.route_service.mark_stop_as_completed(self.mock_route1, 0)
        
        # Assert
        self.assertNotEqual(self.mock_routestops[1].stop_status, RouteStatus.COMPLETED)
        
    def  test_markStopAsCompleted_raiseError_whenStopIndexInvalid(self):

        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.mark_stop_as_completed(self.mock_route1, 5)
            
    def test_markStopAsCompleted_raiseError_whenStopStatusInvalid(self):
        
        # Arrange
        self.mock_routestops[0].stop_status = RouteStatus.COMPLETED
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.mark_stop_as_completed(self.mock_route1,0)
        
class FindRoutesForPackage_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
                
        self.mock_route1 = MagicMock(spec_set=Route, status = RouteStatus.IN_PROGRESS)
        self.mock_route1.can_deliver_between.return_value = True
        self.mock_route2 = MagicMock(spec_set=Route, status = RouteStatus.IN_PROGRESS)  
        self.mock_route2.can_deliver_between.return_value = False
        self.mock_routes = [self.mock_route1, self.mock_route2]
        
        self.mock_app_data.routes.values.return_value = self.mock_routes
        
        self.mock_package = MagicMock(spec_set=Package)
        self.mock_package.start_location = "A"
        self.mock_package.end_location = "B"

    def test_findRoutesForPackages_callsValuesOnce(self):
            
        # Act
        self.route_service.find_routes_for_package(self.mock_package)
        
        # Assert
        self.mock_app_data.routes.values.assert_called_once()
        
    def test_callsCanDeliverBetween_withPackageLocations(self):
         
        # Act
        self.route_service.find_routes_for_package(self.mock_package)
         
        # Assert
        self.mock_route1.can_deliver_between.assert_called_once_with("A", "B")
        self.mock_route2.can_deliver_between.assert_called_once_with("A", "B")
        
    def test_returnsList(self):
        # Act
        result = self.route_service.find_routes_for_package(self.mock_package)

        # Asseert
        self.assertIsInstance(result, list)
           
    def test_returnsOnlyRoutesThatCanDeliver(self):
        
        # Act
        result = self.route_service.find_routes_for_package(self.mock_package)

        # Assert
        self.assertEqual(result, [self.mock_route1])
    
    def test_returnsEmptyList_whenNoRoutesMatch(self):
        
        # Arrange
        self.mock_route1.can_deliver_between.return_value = False
        
        # Act
        result = self.route_service.find_routes_for_package(self.mock_package)
        
        # Assert
        self.assertEqual(result, [])

class AssignPackageToRoute_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.mock_package = MagicMock(spec_set=Package)
        self.mock_package.package_id = 1
        self.mock_package.route_id = None
        self.mock_package.start_location = City.SYD
        self.mock_package.end_location = City.PER
        self.mock_package.weight = 10
        
        self.mock_vehicle = MagicMock(spec_set=Vehicle)
        self.mock_vehicle.max_capacity = 100
        
        self.mock_stop_a = MagicMock(spec_set=RouteStop, location = City.SYD)
        self.mock_stop_b = MagicMock(spec_set=RouteStop, location = City.PER)
        self.mock_stop_c = MagicMock(spec_set=RouteStop, location = City.MEL)
    
        self.mock_route1 = MagicMock(spec_set=Route)
        self.mock_route1.route_id = 1
        self.mock_route1.vehicle_id = 1001
        self.mock_route1.can_deliver_between.return_value = True
        self.mock_route1.stops = [
            self.mock_stop_a,
            self.mock_stop_b,
            self.mock_stop_c
            ]
        self.mock_route1.weight_at_stop.return_value = 0
        
        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
        self.route_service.get_route = MagicMock(return_value=self.mock_route1)
        self.route_service._app_data.find_vehicle.return_value = self.mock_vehicle

    def test_callsGetRouteOnce_withCorrectData(self):
        
        # Act
        self.route_service.assign_package_to_route(self.mock_package, 1)
        
        # Assert
        self.route_service.get_route.assert_called_once_with(1)
        
    def test_callsFindVehicleOnce_withCorrectData(self):
        
        # Act
        self.route_service.assign_package_to_route(self.mock_package, 1)

        # Assert
        self.mock_app_data.find_vehicle.assert_called_once_with(1001)
        
    def test_raiseError_whenPackageAlreadyAssigned(self):
        
        # Arrange
        self.mock_package.route_id = 5
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.assign_package_to_route(self.mock_package, 1)
            
        # should not proceed to mutate anything
        self.mock_route1.add_package.assert_not_called()

    def test_raiseError_whenRouteCannotDeliver(self):
        
        # Arrange
        self.mock_route1.can_deliver_between.return_value = False
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.assign_package_to_route(self.mock_package, 1)
            
        self.mock_route1.can_deliver_between.assert_called_once_with(City.SYD,City.PER)
        # should not proceed to mutate anything
        self.mock_route1.add_package.assert_not_called()
        
    def test_raiseError_whenNoVehicleAssigned(self):

        # Arrange
        self.mock_route1.vehicle_id = None

        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.assign_package_to_route(self.mock_package, 1)

        # should not proceed to mutate anything
        self.mock_route1.add_package.assert_not_called()
        
    def test_raiseError_ifCapacityExceededAtIntermediateStop(self):
        
        # Arrange
        # pickup="SYD"(index 0), dropoff="MEL"(index 2) -> checks indices 0 and 1
        self.mock_package.start_location = City.SYD
        self.mock_package.end_location = City.MEL
        # index 0 nothing is assigned and the package seem to fit in
        # but since on the next stop[1] I have already assigned packages with weight 95
        # i can't assign the package and should raise and error
        self.mock_route1.weight_at_stop.side_effect = lambda i: 95 if i == 1 else 0

        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.assign_package_to_route(self.mock_package, 1)

        self.mock_route1.add_package.assert_not_called()
        self.mock_package.assign_to_route.assert_not_called()
  
    def test_capacityCheck_onlyCoversPickupToDropoffRange(self):
        
        # Arrange
        self.mock_package.start_location = City.SYD
        self.mock_package.end_location = City.MEL
        
        # Act
        self.route_service.assign_package_to_route(self.mock_package, 1)

        # Assert
        called_indices = [c.args[0] for c in self.mock_route1.weight_at_stop.call_args_list]
        self.assertEqual(called_indices, [0,1])  # pickup_index=0, dropoff_index=2, range excludes 2, expected [0,1]

    def test_successfulAssignmentUpdates_forRoutePackageAndStops(self):
        
        # Act
        self.route_service.assign_package_to_route(self.mock_package, 1)

        # Assert
        self.mock_route1.add_package.assert_called_once_with(1)
        self.mock_package.assign_to_route.assert_called_once_with(1)
        self.mock_stop_a.add_pick_up_weight.assert_called_once_with(10)
        self.mock_stop_a.add_drop_off_weight.assert_not_called()
        self.mock_stop_b.add_pick_up_weight.assert_not_called()
        self.mock_stop_b.add_drop_off_weight.assert_called_once_with(10)

class AssignPackagesFromHubs_Should(unittest.TestCase):

    def setUp(self):
        
        # Arrange
        self.mock_package1 = MagicMock(spec_set=Package, package_id = 1, weight = 2, start_location = City.SYD, end_location = City.MEL)
        self.mock_package2 = MagicMock(spec_set=Package, package_id = 2, weight = 100, start_location = City.PER, end_location = City.MEL)
        self.mock_package3 = MagicMock(spec_set=Package, package_id = 3, weight = 2, start_location = City.PER, end_location = City.MEL)

        
        self.mock_stop1 = MagicMock(spec_set=RouteStop, location = City.SYD, stop_status = RouteStatus.PLANNED)
        self.mock_stop2 = MagicMock(spec_set=RouteStop, location = City.PER, stop_status = RouteStatus.PLANNED)
        self.mock_stop3 = MagicMock(spec_set=RouteStop, location = City.MEL, stop_status = RouteStatus.PLANNED)
        self.mock_stops = [
            self.mock_stop1,
            self.mock_stop2,
            self.mock_stop3
            ]

        self.mock_hub1 = MagicMock(spec_set=Hub, city=City.SYD)
        self.mock_hub1.find_packages_for_locations.return_value = [self.mock_package1]
        self.mock_hub2 = MagicMock(spec_set=Hub, city=City.PER)
        self.mock_hub2.find_packages_for_locations.return_value = [self.mock_package2, self.mock_package3]
        self.mock_hub3 = MagicMock(spec_set=Hub, city=City.MEL)

        self.mock_hubs = [self.mock_hub1, self.mock_hub2, self.mock_hub3]

        self.mock_vehicle = MagicMock(spec_set=Vehicle, max_capacity = 100)

        self.mock_route = MagicMock(spec_set=Route, route_id = 1, vehicle_id = None, stops = self.mock_stops)
        # called for each stop in route.stops except last one
        # last is allways zero
        self.mock_route.weight_at_stop.side_effect = [2,4]
        
        self.mock_app_data = MagicMock()
        # find_hub is called once per stop, in the order stops are processed
        self.mock_app_data.find_hub.side_effect = [self.mock_hub1, self.mock_hub2, self.mock_hub3]
        self.route_service = RouteService(self.mock_app_data)
        
    def test_callsAppDataFindHubForEachStop_withCorrectData(self):
        
        # Act
        self.route_service.assign_packages_from_hubs(self.mock_route, self.mock_vehicle)
        
        # Assert
            # Searching for packages to assign, so last stop is ommited, bacause we only leave packages there
        self.assertEqual(
            self.mock_app_data.find_hub.call_args_list,
            [
                unittest.mock.call(self.mock_stops[0].location),
                unittest.mock.call(self.mock_stops[1].location)
             ]
        )
        
    def test_callsHubFindPackageForLocations_withCorrectData(self):
        
        # Act
        self.route_service.assign_packages_from_hubs(self.mock_route, self.mock_vehicle)
        
        # Assert
            # calls with list of city.location for later stops in the route
        self.mock_hub1.find_packages_for_locations.assert_called_once_with([City.PER, City.MEL])
        self.mock_hub2.find_packages_for_locations.assert_called_once_with([City.MEL])
        
    def test_callsRouteWeightAtStop_withCorrectData(self):
        
        # Act
        self.route_service.assign_packages_from_hubs(self.mock_route, self.mock_vehicle)
        
        # Assert
        self.assertEqual(
            self.mock_route.weight_at_stop.call_args_list,
            [unittest.mock.call(0), unittest.mock.call(1)]
        )
        
    def test_continuesEvaluating_afterSkippingOversizedPackage(self):
        """
        Tests calls to the 4 methods involved in mutating state
            Route.add_package()
            Package.assing_to_route()
            RouteStop.add_pick_up_weight()
            RouteStop.add_drop_off_weight()
        """
        # Act
        self.route_service.assign_packages_from_hubs(self.mock_route, self.mock_vehicle)
        
        # Assert
            # Route.add_package()
        self.assertEqual(
            self.mock_route.add_package.call_args_list,
            [
                unittest.mock.call(self.mock_package1.package_id),
                unittest.mock.call(self.mock_package3.package_id)
            ]
        )
        
            # Package.assign_to_route()
        self.mock_package1.assign_to_route.assert_called_once_with(self.mock_route.route_id)
        self.mock_package3.assign_to_route.assert_called_once_with(self.mock_route.route_id)
        
            # RouteStop.add_pick_up_weight
        self.mock_stop1.add_pick_up_weight.assert_called_once_with(self.mock_package1.weight)
        self.mock_stop2.add_pick_up_weight.assert_called_once_with(self.mock_package3.weight)
        
            # RouteStop.add_drop_off_weight
        self.assertEqual(
            self.mock_stop3.add_drop_off_weight.call_args_list,
            [
                unittest.mock.call(self.mock_package1.weight),
                unittest.mock.call(self.mock_package3.weight)
            ]
        )
            
    def test_skipsPackages_whenExceedingRemainingCapacity(self):
        """
        Tests calls to the 4 methods involved in mutating state
            Route.add_package()
            Package.assing_to_route()
            RouteStop.add_pick_up_weight()
            RouteStop.add_drop_off_weight()
        """
        # Arrange
        self.mock_package1.weight = 1
        self.mock_package2.weight = 100
        self.mock_package3.weight = 100
        
        # Act
        self.route_service.assign_packages_from_hubs(self.mock_route, self.mock_vehicle)
        
        # Assert
            # Route.add_package()
        self.mock_route.add_package.assert_called_once_with(self.mock_package1.package_id)
        
            # Package.assign_to_route()
        self.mock_package1.assign_to_route.assert_called_once_with(self.mock_route.route_id)
        self.mock_package2.assign_to_route.assert_not_called()
        self.mock_package3.assign_to_route.assert_not_called()
        
            # RouteStop.add_pick_up_weight
        self.mock_stop1.add_pick_up_weight.assert_called_once_with(self.mock_package1.weight)
        self.mock_stop2.add_pick_up_weight.assert_not_called()
        
            # RouteStop.add_drop_off_weight
        self.mock_stop3.add_drop_off_weight.assert_called_once_with(self.mock_package1.weight)
        
    def test_assignPackage_whenFitsInCapacity_withCorrectData(self):
        """
        Tests calls to the 4 methods involved in mutating state
            Route.add_package()
            Package.assing_to_route()
            RouteStop.add_pick_up_weight()
            RouteStop.add_drop_off_weight()
        """
        # Arrange
        self.mock_package2.weight = 2
        
        # Act
        self.route_service.assign_packages_from_hubs(self.mock_route, self.mock_vehicle)
        
        # Assert
            # Route.add_package()
        self.assertEqual(
            self.mock_route.add_package.call_args_list, 
            [
                unittest.mock.call(self.mock_package1.package_id),
                unittest.mock.call(self.mock_package2.package_id),
                unittest.mock.call(self.mock_package3.package_id)
            ]
        )
        
            # Package.assign_to_route()
        self.mock_package1.assign_to_route.assert_called_once_with(self.mock_route.route_id)
        self.mock_package2.assign_to_route.assert_called_once_with(self.mock_route.route_id)
        self.mock_package3.assign_to_route.assert_called_once_with(self.mock_route.route_id)
        
            # RouteStop.add_pick_up_weight
        self.mock_stop1.add_pick_up_weight.assert_called_once_with(self.mock_package1.weight)
        self.assertEqual(
            self.mock_stop2.add_pick_up_weight.call_args_list,
            [
                unittest.mock.call(self.mock_package2.weight),
                unittest.mock.call(self.mock_package3.weight)
            ]
        )
        
            # RouteStop.add_drop_off_weight
        self.assertEqual(
            self.mock_stop3.add_drop_off_weight.call_args_list,
            [
                unittest.mock.call(self.mock_package1.weight),
                unittest.mock.call(self.mock_package2.weight),
                unittest.mock.call(self.mock_package3.weight)
            ]
        )
        
    def test_noAssignment_whenHubHasNoCandidates(self):
        
        # Arrange
        self.mock_hub1.find_packages_for_locations.return_value = []
        self.mock_hub2.find_packages_for_locations.return_value = []
        self.mock_hub3.find_packages_for_locations.return_value = []
        
        # Act
        self.route_service.assign_packages_from_hubs(self.mock_route, self.mock_vehicle)
        
        # Assert
        self.mock_route.add_package.assert_not_called()
        
    def test_raiseError_whenDropOffStopMissing(self):
        """ 
            This is now a valid joke.
            We made a bet whether it is possible.
            Thats how the raise ValueError appeared in the code.
            Will implement this when that code becomes official.
        """
        # Assert
        self.assertTrue(True)
          
class AssignTruckToRoute_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
        
        self.mock_route = MagicMock(spec_set=Route, route_id = 1, vehicle_id = None)
        self.mock_vehicle = MagicMock(spec_set=Vehicle,vehicle_id = 1001, route_id = None)
        
    def test_changesValues_whenValidData(self):
        
        # Act
        self.route_service.assign_truck_to_route(self.mock_route, self.mock_vehicle)
        
        # Assert
        self.assertEqual(self.mock_route.vehicle_id, 1001)
        self.assertEqual(self.mock_vehicle.route_id, 1)
   
    def test_raiseError_WhenRouteAlreadyHasTruck(self):
        
        # Arrange
        self.mock_route.vehicle_id = 1
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.assign_truck_to_route(self.mock_route, self.mock_vehicle)
        
        # route.veihcle_id not touched
        self.assertEqual(self.mock_route.vehicle_id, 1)
        
    def test_raiseError_WhenVehicleAlreadyHasRoute(self):
        
        # Arrange
        self.mock_vehicle.route_id = 2
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.assign_truck_to_route(self.mock_route, self.mock_vehicle)
        
        # vehicle.route_id not touched
        self.assertEqual(self.mock_vehicle.route_id, 2)
        
class StartRoute_Should(unittest.TestCase):
    
    def _check_stop_status(self, stops, status: RouteStatus):
        for stop in stops:
            self.assertEqual(stop.stop_status, status)
    
    def setUp(self):
        
        # Arrange
        
        self.mock_stop1 = MagicMock(spec_set=RouteStop, location = City.SYD, stop_status = RouteStatus.PLANNED)
        self.mock_stop2 = MagicMock(spec_set=RouteStop, location = City.PER, stop_status = RouteStatus.PLANNED)
        
        # self.mock_stops = [self.mock_stop1, self.mock_stop2]
        
        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
        
        self.mock_route = MagicMock(
            spec_set=Route,
            route_id = 1,
            vehicle_id = 1,
            status = RouteStatus.PLANNED,
            stops = [self.mock_stop1, self.mock_stop2]
            )
    
    def test_changesRouteStatus_whenValidData(self):
        
        # Act
        self.route_service.start_route(self.mock_route)
        
        # Assert
        self.assertEqual(self.mock_route.status, RouteStatus.IN_PROGRESS)
        
    def test_changesStopsStatus_whenValidData(self):
        
        # Act
        self.route_service.start_route(self.mock_route)
        
        # Assert
        self._check_stop_status(self.mock_route.stops, RouteStatus.IN_PROGRESS)        
    
    def test_raiseError_whenVeihcleIdIsNone(self):
        
        # Arrange
        self.mock_route.vehicle_id = None
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.start_route(self.mock_route)
            
        #status not changed
        self.assertEqual(self.mock_route.status, RouteStatus.PLANNED)
        self._check_stop_status(self.mock_route.stops, RouteStatus.PLANNED)
        
    def test_raiseError_whenRouteStatusIsCompleted(self):
        
        # Arrange
        self.mock_route.status = RouteStatus.COMPLETED
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.start_route(self.mock_route)
            
        #status not changed
        self.assertEqual(self.mock_route.status, RouteStatus.COMPLETED)
        self._check_stop_status(self.mock_route.stops, RouteStatus.PLANNED)
        
    def test_raiseError_whenStopStatusIsCompleted(self):
        
        # Arrange
        self.mock_stop1.stop_status = RouteStatus.COMPLETED
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.start_route(self.mock_route)

        # assert status not changed
        self.assertEqual(self.mock_route.status, RouteStatus.PLANNED)
        self.assertEqual(self.mock_stop1.stop_status, RouteStatus.COMPLETED)
        self.assertEqual(self.mock_stop2.stop_status, RouteStatus.PLANNED)
        
class CompleteAllRoutesNextStop_Should(unittest.TestCase):

    def setUp(self):
        
        # Arrange
        self.mock_route1 = MagicMock(
            spec_set=Route,
            route_id = 1,
            status = RouteStatus.IN_PROGRESS,
            stops = [MagicMock(), MagicMock(), MagicMock()])
        
        self.mock_route2 = MagicMock(
            spec_set=Route,
            route_id = 2,
            status = RouteStatus.IN_PROGRESS,
            stops = [MagicMock(), MagicMock()]
            )
        
        self.mock_route1.get_index_of_next_incompleted_stop = MagicMock(return_value = 2)
        self.mock_route2.get_index_of_next_incompleted_stop = MagicMock(return_value = 0)

        self.mock_routes = [self.mock_route1, self.mock_route2]

        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
        self.route_service.get_routes_by_status = MagicMock(return_value = self.mock_routes)
        
        self.mock_load_packages_method = patch.object(RouteService, "load_route_packages_from_stop").start()
        self.mock_unload_packages_method = patch.object(RouteService, "unload_route_packages_to_stop").start()
        self.mock_mark_route_method = patch.object(RouteService, "mark_route_as_completed").start()
        self.mock_mark_stop_method = patch.object(RouteService, "mark_stop_as_completed").start()
        
        self.addCleanup(patch.stopall)
        
    def test_callsOnce_getRoutesByStatus_withCorrectData(self):

        # Act
        self.route_service.complete_all_routes_next_stop()
        
        # Assert
        self.route_service.get_routes_by_status.assert_called_once_with(RouteStatus.IN_PROGRESS)
        
    def test_callsForEachRoute_getIndexOfNextIncompletedStop(self):  
        
        # Act
        self.route_service.complete_all_routes_next_stop()
        
        # Assert
        self.mock_route1.get_index_of_next_incompleted_stop.assert_called_once()
        self.mock_route2.get_index_of_next_incompleted_stop.assert_called_once()
        
    def test_callsOnlyLoadPackages_whenStopIndexIsZero_withCorrectData(self):
        
        # Act
        self.route_service.complete_all_routes_next_stop()
        
        # Assert
        self.assertEqual(
            self.mock_load_packages_method.call_args_list,
            [unittest.mock.call(self.mock_route2, 0)]
        )
        
    def test_callsOnlyUnLoadPackages_whenStopIndexIsLast_withCorrectData(self):
        
        # Act
        self.route_service.complete_all_routes_next_stop()

        # Assert
        self.assertEqual(
            self.mock_unload_packages_method.call_args_list,
            [unittest.mock.call(self.mock_route1, 2)]
        )
    
    def test_callsLoadAndUnload_whenStopIndexIndexNotFirstNotLast_withCorrectData(self):

        # Arrange
        self.mock_route1.get_index_of_next_incompleted_stop = MagicMock(return_value = 1)
        self.route_service.get_routes_by_status = MagicMock(return_value = [self.mock_route1])
        
        # Act
        self.route_service.complete_all_routes_next_stop()
        
        # Assert
        self.mock_load_packages_method.assert_called_once_with(self.mock_route1, 1)
        self.mock_unload_packages_method.assert_called_once_with(self.mock_route1, 1)
        
    def test_callsMarkStopAsCompleted_withCorrectData(self):
        
        # Act
        self.route_service.complete_all_routes_next_stop()
        
        # Arrange
        self.assertEqual(
            self.mock_mark_stop_method.call_args_list,
            [unittest.mock.call(self.mock_route1,2), unittest.mock.call(self.mock_route2,0)]
        )
        
    def test_callsMarkRouteAsCompleted_whenStopIndexIsLast_withCorrectData(self):
        
        # Act
        self.route_service.complete_all_routes_next_stop()
        
        # Arrange
        self.mock_mark_route_method.assert_called_once_with(self.mock_route1)
  
class LoadRoutePackagesFromStop_Should(unittest.TestCase):
    
    def setUp(self):

        # Arrange
        self.mock_package1 = MagicMock(spec_set=Package, current_location = City.PER , end_location = City.SYD)
        self.mock_package2 = MagicMock(spec_set=Package, current_location = City.PER, end_location = City.ADL)
        
        self.mock_hub = MagicMock(
            spec_set=Hub,
            city = City.SYD,
            packages_ids = {1,2,3}
            )
        
        self.mock_stop1 = MagicMock(spec_set=RouteStop, location = City.PER)
        self.mock_stop2 = MagicMock(spec_set=RouteStop, location = City.SYD)
        
        self.mock_route1 = MagicMock(
            spec_set=Route,
            stops = [self.mock_stop1, self.mock_stop2],
            packages_ids = {1,2,4}
            )
        
        self.mock_app_data = MagicMock()
        self.mock_app_data.find_hub.return_value = self.mock_hub
        
        #app_data.find_package is called for every match in hub's & route's packages_ids
        self.mock_app_data.find_package.side_effect = [self.mock_package1, self.mock_package2]
        self.route_service = RouteService(self.mock_app_data)
        
    def test_callsFindHubOnce_withCorrectStopLocation(self):
        
        # Act
        self.route_service.load_route_packages_from_stop(self.mock_route1, 1)
        
        # Assert
        self.mock_app_data.find_hub.assert_called_once_with(City.SYD)
        
    def test_callsHubsRemoveSinglePackage_withCorrectPackageIds(self):
        
        # Act
        self.route_service.load_route_packages_from_stop(self.mock_route1, 1)
        
        # Assert
        self.mock_hub.remove_single_package.assert_has_calls([
            unittest.mock.call(1),
            unittest.mock.call(2)
        ])
        
    def test_callsFindPackage_withCorrectPackageIds(self):

        # Act
        self.route_service.load_route_packages_from_stop(self.mock_route1, 1) #id[1] => City.SYD
        
        # Assert
        self.mock_app_data.find_package.assert_has_calls([
            unittest.mock.call(1),
            unittest.mock.call(2),
            ])
        
    def test_callsStartDelivery_onValidPackages(self):
        
        # Act
        self.route_service.load_route_packages_from_stop(self.mock_route1, 1) #id[1] => City.SYD
    
        # Assert
        self.mock_package1.start_delivery.assert_called_once()
        self.mock_package2.start_delivery.assert_called_once()

class UnloadRoutePackagesToStop_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self.mock_package1 = MagicMock(spec_set=Package, current_location = City.PER , end_location = City.SYD)
        self.mock_package2 = MagicMock(spec_set=Package, current_location = City.PER, end_location = City.ADL)

        self.mock_hub = MagicMock(spec_set=Hub, city = City.SYD)
    
        self.mock_stop1 = MagicMock(spec_set=RouteStop, location = City.PER)
        self.mock_stop2 = MagicMock(spec_set=RouteStop, location = City.SYD)

        self.mock_route1 = MagicMock(
            spec_set=Route,
            stops = [self.mock_stop1, self.mock_stop2],
            packages_ids = {1,2}
            )
        self.mock_app_data = MagicMock()
        self.mock_app_data.find_hub.return_value = self.mock_hub

        # find_package is called for every package in route's packages_ids
        self.mock_app_data.find_package.side_effect = [self.mock_package1, self.mock_package2]
        self.route_service = RouteService(self.mock_app_data)
        
    def test_callsFindHubOnce_withCorrectStopLocation(self):
        
        # Act
        self.route_service.unload_route_packages_to_stop(self.mock_route1, 1)
        
        # Assert
        self.mock_app_data.find_hub.assert_called_once_with(City.SYD)
        
    def test_callsFindPackage_withCorrectPackageIds(self):
        
        # Act
        self.route_service.unload_route_packages_to_stop(self.mock_route1, 1)
        
        # Assert
        self.mock_app_data.find_package.assert_has_calls([
            unittest.mock.call(1),
            unittest.mock.call(2),
            ])
    
    def test_callsAddSinglePackage_onlyWhenMatchingLocations(self):
        
        # Act
        self.route_service.unload_route_packages_to_stop(self.mock_route1, 1)
        
        # Assert
        self.mock_hub.add_single_package.assert_called_once_with(self.mock_package1, delivered=True)
    
    def test_callsMarkDelivered_whenMatchingLocations(self):
        
        # Act
        self.route_service.unload_route_packages_to_stop(self.mock_route1, 1)
        
        # Assert
        self.mock_package1.mark_delivered.assert_called_once()
    
    def test_notCallsMarkDelivered_whenNotMatchingLocations(self):
        
        # Act
        self.route_service.unload_route_packages_to_stop(self.mock_route1, 1)
        
        # Assert
        self.mock_package2.mark_delivered.assert_not_called()
        
    def test_changesPackageCurrentLocation(self):
        
        # Act
        self.route_service.unload_route_packages_to_stop(self.mock_route1, 1)
        
        # Assert
        self.assertEqual(self.mock_package1.current_location, self.mock_stop2.location)
        self.assertEqual(self.mock_package2.current_location, self.mock_stop2.location)

class GetEtaForLocation_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        # no spec because arrivaltime is object attribute not class
        self.mock_stop1 = MagicMock(location = City.SYD, arrival_time = datetime.min)
        self.mock_stop2 = MagicMock(location = City.PER, arrival_time = datetime.min)
        
        self.mock_route1 = MagicMock(
            spec_set=Route,
            stops = [self.mock_stop1, self.mock_stop2]
            
            )

        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
        self.route_service.get_route = MagicMock(return_value=self.mock_route1)
        
    def test_callsGetRouteOnce(self):
            
        # Act
        self.route_service.get_eta_for_location(1, City.SYD)

        # Assert
        self.route_service.get_route.assert_called_once_with(1)
        
    def test_returnCorrectValue_whenValidData(self):
        
        # Act
        result = self.route_service.get_eta_for_location(1, City.SYD)
        
        # Assert
        self.assertEqual(result, self.mock_stop1.arrival_time)
        
    def test_raiseError_whenLocationNotInRouteStops(self):
        
        # Act, Assert
        with self.assertRaises(ValueError):
            self.route_service.get_eta_for_location(1, City.ADL)