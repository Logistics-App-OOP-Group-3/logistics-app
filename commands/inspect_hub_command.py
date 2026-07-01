from commands.base.base_command import BaseCommand
import commands.validation_helper as vh 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.application_data import ApplicationData
    from services.hub_service import HubService
class InspectHubCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData, hub_service: HubService):
        vh.validate_params_count(params, 1, "InspectHubCommand")
        super().__init__(params, app_data)
        self._hub_service = hub_service
        
    def execute(self):
        hub_city = vh.try_parse_city(self.params[0])
        hub = self._app_data.find_hub(hub_city)
        
        return hub.info_unassigned_packages_by_end_location()
        