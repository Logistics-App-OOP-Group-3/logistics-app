from commands.base.base_command import BaseCommand
from services.package_service import PackageService
from enums.package_status import PackageStatus

class UnassignedPackagesCommand(BaseCommand):

    def __init__(self, params, app_data, package_service: PackageService):
        super().__init__(params, app_data)
        self._package_service = package_service

    def execute(self):
        """Show all unassigned packages 1 per line"""

        packages = self._package_service.get_packages_by_status(PackageStatus.NOT_ASSIGNED)

        return '\n'.join([p.short_info() for p in packages])
