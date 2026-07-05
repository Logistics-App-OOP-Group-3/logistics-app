from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count, try_parse_int
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services.package_service import PackageService


class PackageInfoCommand(BaseCommand):

    def __init__(self, params, app_data, package_service: PackageService):
        # Expected input: <package_id>
        validate_params_count(params, 1, "PackageInfoCommand")
        super().__init__(params, app_data)
        self._package_service = package_service

    def execute(self):
        package_id = try_parse_int(self.params[0])
        package = self._package_service.get_package(package_id)

        return str(package)