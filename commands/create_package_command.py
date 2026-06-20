from commands.base.base_command import BaseCommand

class CreatePackageCommand(BaseCommand):
    def __init__(self, params, app_data, package_service, route_service):
        super().__init__(params, app_data)
        self._package_service = package_service
        self._route_service = route_service
    
    def execute(self):
        
        start_location = self.params[0]
        end_location = self.params[1]
        weigth = float(self.params[2])
        contact_info = self.params[3]
        
        package = self._package_service.create_package(
            start_location,
            end_location,
            weight,
            contact_info
        )
        
        routes = self._route_service.find_routes_for_package(package)
        
        result = [
            "Package created.",
            f"Package ID: {package.package_id}",
            f"From: {start_location} -> To: {end_location}",
            f"Weight: {weight} kg"
        ]
        
        if routes:
            result.append("Matching routes:")
            
            for route in routes:
                result.append(
                    f"- Route {route.route_id}: "
                    f"{route.start_location} -> {route.end_location}"
                )
        else:
            result.append("No suitable routes")
            
        return "\n".join(result)

        

