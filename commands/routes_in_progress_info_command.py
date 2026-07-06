from __future__ import annotations
from commands.base.base_command import BaseCommand
from enums.route_status import RouteStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.route_service import RouteService

class RoutesInProgressInfoCommand(BaseCommand):
    
    def __init__(self, params, app_data, route_service: 'RouteService'):
        super().__init__(params, app_data)
        self._route_service = route_service

    def execute(self):
        routes = self._route_service.get_routes_by_status(RouteStatus.IN_PROGRESS)
        
        if not routes:
            return "No routes are currently in progress."
        
        result = ["--- Routes In Progress ---"]
        for route in routes:
            result.append(str(route))
            result.append("-" * 30)
            
        return "\n".join(result)