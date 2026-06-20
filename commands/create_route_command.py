from base.base_command import BaseCommand

class CreateRouteCommand(BaseCommand):
    
    def __init__(self, params, app_data, route_service):
        super().__init__(params, app_data)
        self._route_service = route_service
        
    def execute(self):
        
        stops = list(self.params)
        
        route = self._route_service.create_route(stops)
        
        return (
        f"Route created successfully. \n"
        f"Route ID: {route.route_id}"
        f"Stops: {" -> ".join(stops)}"
        )
        
    