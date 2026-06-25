from commands.base.base_command import BaseCommand


class UnassignedPackagesCommand(BaseCommand):

    def __init__(self, params, app_data, package_service):
        # No parameters required
        super().__init__(params, app_data)
        self._package_service = package_service

    def execute(self):

        # Lists all packages that are not assigned to any route
        # Should filter by:
        # - package.route_id is None OR status == NOT_ASSIGNED

        packages = self._package_service.get_all_packages()

        result = []

        for p in packages:
            if p.route_id is None:
                result.append(f"{p.package_id}: {p.start_location} -> {p.end_location}")

        return "\n".join(result) if result else "No unassigned packages"