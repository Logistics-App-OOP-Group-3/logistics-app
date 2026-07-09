import unittest
from unittest.mock import MagicMock, patch
from services.route_service import RouteService
from enums.route_status import RouteStatus
from enums.city import City
from models.route.route import Route
from models.package import Package
from models.vehicle import Vehicle

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
                
        self.mock_route1 = MagicMock(spec_set=Route)
        self.mock_route1.can_deliver_between.return_value = True
        self.mock_route2 = MagicMock(spec_set=Route)  
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
        self.mock_stop_a.add_pick_up_weigth.assert_called_once_with(10)
        self.mock_stop_a.add_drop_off_weigth.assert_not_called()
        self.mock_stop_b.add_pick_up_weigth.assert_not_called()
        self.mock_stop_b.add_drop_off_weigth.assert_called_once_with(10)


class AssignPackagesFromHubs_Should(unittest.TestCase):
    
    def setUp(self):
        
        self.mock_app_data = MagicMock()
        self.route_service = RouteService(self.mock_app_data)
        