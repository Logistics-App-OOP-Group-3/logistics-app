from __future__ import annotations
from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.route_service import RouteService
    from core.application_data import ApplicationData

class AdvanceRoutesCommand(BaseCommand):
    """
    SIMULATION COMMAND
    input_trigger: advanceroutes
    execution:
        Completes next stop for each route IN_PROGRESS
    """
    
    def __init__(self,params, app_data: ApplicationData, route_service: RouteService):
        validate_params_count(params, 0, "AdvanceRoutesCommand")
        super().__init__(params, app_data)
        self._route_service = route_service
    
    def execute(self):
        self._route_service.complete_all_routes_next_stop()
        
        return f"All routes advanced to their next stop.\n"