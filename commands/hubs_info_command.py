from __future__ import annotations
from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.hub_service import HubService
    from core.application_data import ApplicationData

class HubInfoCommand(BaseCommand):
    """
    input_trigger: hubsinfo
    execution:
        Shows unassigned packages total weight and count in each hub,
        sorted by weight and then count.
    """
    
    def __init__(self, params, app_data: ApplicationData, hub_service: HubService):
        validate_params_count(params, 0, "HubInfoCommand")
        super().__init__(params, app_data)
        self._hub_service = hub_service

    def execute(self):
        
        return self._hub_service.info_not_assigned_packages_by_city()
        
        