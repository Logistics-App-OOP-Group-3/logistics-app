from commands.base.base_command import BaseCommand
from commands.validation_helper import validate_params_count


class PackageInfoCommand(BaseCommand):

    def __init__(self, params, app_data, package_service):
        # Expected input: <package_id>
        validate_params_count(params, 1, "PackageInfoCommand")
        super().__init__(params, app_data)
        self._package_service = package_service

    def execute(self):

        package_id = int(self.params[0])

        # Displays detailed package information
        # Should include:
        # - package details
        # - status (NOT_ASSIGNED / ASSIGNED / IN_TRANSIT / DELIVERED)
        # - assigned route if any

        package = self._package_service.get_package(package_id)

        result = [
            str(package),
            f'Weight: {package.weight} kg',
            f'Contact: {package.contact_info}'         
        ] 

        if package.route_id is None:
            result.append('Route: Not Assigned')
        else:
            result.append(f'Route: {package.route_id}')

        return '\n'.join(result)