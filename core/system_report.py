
# from core.application_data import ApplicationData
# from enums.vehicle_status import VehicleStatus
# from models.vehicle import Vehicle

# class SystemReport:
    
#     def __init__(self, app_data: ApplicationData):
#         self._app_data = app_data
    
   
    
#     # Test Method
#     def info_vehicle_storage(self) -> str:
#         result = []
#         for vehicle in self._app_data.vehicles:
#             result.append(str(vehicle))
#         return '\n'.join(result)
    

#     def info_not_assigned_packages(self) -> str:
#         result = []
#         result.append("List of unassigned packages:")
#         for id, package in self._packages:
#             if package.status == "NotAssigned":
#                 result.append(f" Package: {id} at {package.current_location} city")
#         return '\n'.join(result)