import unittest
from unittest.mock import MagicMock, patch
from services.route_service import RouteService
from enums.route_status import RouteStatus
from models.route.route import Route
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
            
    def test_markStopAsCompleted_changesStatus_whenValidData(self):
        
        # Act
        self.route_service.mark_stop_as_completed(self.mock_route1, 0)

        # Assert
        self.assertEqual(self.mock_routestops[0].stop_status, RouteStatus.COMPLETED)

    def test_markStopAsCompleted_notChangesStatusOfOtherStops(self):

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
                    
 
