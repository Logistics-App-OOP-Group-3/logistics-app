from models.package.package import Package
from enums.package_status import PackageStatus

class PackageService:
    
    ### Handles all the business logic related to packages
    ### Responsible for creating and retrieving packages
    ### Also responsible for filtering packages by status
    def __init__(self, app_data):
        self.app_data = app_data

    def create_package(
        self,
        start_location: str,
        end_location: str,
        weight: float,
        contact_info: str
    ):
        package_id = self.app_data.generate_package_id()

        package = Package(
            package_id,
            start_location,
            end_location,
            weight,
            contact_info
        )

        self.app_data.add_package(package)
        return package

    def get_package(self, package_id: int):
        return self.app_data.find_package(package_id)

    def get_all_packages(self):
        return list(self.app_data.packages.values())

    def get_packages_by_status(self, status: PackageStatus):
        return [
            p for p in self.app_data.packages.values()
            if p.status == status
        ]

    def mark_in_transit(self, package_id: int):
        package = self.get_package(package_id)

        if package.status == PackageStatus.DELIVERED:
            raise ValueError("Delivered package cannot be modified")

        package.status = PackageStatus.IN_TRANSIT

    def mark_delivered(self, package_id: int):
        package = self.get_package(package_id)

        package.status = PackageStatus.DELIVERED