
#TODO : import model classes

# This class holds all objects from our models classes
# Most of the methods about bussiness logic should be defined here
class ApplicationData:
    def __init__(self):
        self._id_package = 0 # UID for creating package
        self._id_routes = 0   # UID for creating route
        
        self._packages: dict[int, object] = dict()
        self._routes: dict[int,object] = dict()
        self._vehicles: dict[int, object] = dict()
        

#TODO: Create interface of methods for the command classes
    
    def find_package(self, id:int) -> object: #TODO:
        if id not in self._packages:
            raise ValueError(f"Package id: {id} cannot be found in the system.")
        return self._packages[id]
    
    def find_route(self, id:int) -> object: #TODO:
        if id not in self._routes:
            raise ValueError(f"Route id: {id} cannt be found in the system.")
        return self._routes[id]
    
    def create_package(self) -> object: #TODO: 
        id = self._generate_package_id
    
        package = None #TODO: delete this line
        #package = Package() #TODO: add args
        return package
        
    def create_route(self, starting_location, delivery_locations:list[object]) -> object: #TODO:
        id = self._generate_route_id

        route = None #TODO: delete this line
        # route = Route()#TODO: add args
        return route
    
    def info_not_assigned_packages(self) -> str:
        result = []
        result.append("List of unassigned packages:")
        for id, package in self._packages:
            if package.status == "NotAssigned":
                result.append(f" Package: {id} at {package.current_location} city")
        return '\n'.join(result)
    
    
    def _generate_package_id(self):
        self._id_package += 1
        return self._id_package
    
    def _generate_route_id(self):
        self._id_routes += 1
        return self._id_routes
    
    
    
    
    
    