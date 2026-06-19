
#TODO : import model classes

# This class holds all objects from our models classes
# Most of the methods about bussiness logic should be defined here
class ApplicationData:
    def __init__(self):
        self._id_package = 0 # UID for creating package
        self._id_route = 0   # UID for creating route
        self._packages: dict[int, object] = dict()
        self._routes: dict[int,object] = dict()
        
        
    def create_package(self) -> object:
        id = self._generate_package_id
    
        package = None #TODO: delete this line
        #package = Package() #TODO: add args
    def create_route(self, starting_location, delivery_locations:list[object]) -> object:
        id = self._generate_route_id

        route = None #TODO: delete this line
        # route = Route()#TODO: add args
        return route
    
    def _generate_package_id(self):
        self._id_package += 1
        return self._id_package
    
    def _generate_route_id(self):
        self._id_route += 1
        return self._id_route
    
    
    #TODO: Create interface of methods for the command classes
    
    
    
    