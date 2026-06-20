from commands.base.base_command import BaseCommand

"""
# Use case 1
accepted_date = datetime.now()
start_location = args[0]
end_location = args[1]
weigth = args[2]
contact_information = args[3]
Validate input
Package.__init__
app.data.add(package)

routes = RouteService.searchRoutes(start_location, end_location)

display routes
if (accept route )
assign package in route
update expected_arival time of package

"""

class CreatePackageCommand(BaseCommand):
    
    def execute(self):
        start_location = self.params[0]
        end_location = self.params[1]
        weigth = float(self.params[2])
        contanct_info = self.params[3]
        
        package = Package(start_location, end_location, weigth)

        

