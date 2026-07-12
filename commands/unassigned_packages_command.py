from commands.base.base_command import BaseCommand
from services.package_service import PackageService
from enums.package_status import PackageStatus
from commands.validation_helper import validate_params_count

class UnassignedPackagesCommand(BaseCommand):
    """
    input_trigger: unassignedpackages
    execution:
        Show all unassigned packages 1 per line
    """
    

    def __init__(self, params, app_data, package_service: PackageService):
        validate_params_count(params, 0, "UnassignedPackagesCommand")
        super().__init__(params, app_data)
        self._package_service = package_service

    def execute(self):

        packages = self._package_service.get_packages_by_status(PackageStatus.NOT_ASSIGNED)

        return '\n'.join([p.short_info() for p in packages])
