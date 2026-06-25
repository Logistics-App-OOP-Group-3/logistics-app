from enum import Enum

class PackageStatus(Enum):
    NOT_ASSIGNED = "Not Assigned"
    ASSIGNED = "Assigned"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"