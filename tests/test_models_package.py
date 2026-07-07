import unittest
from models.package import Package
from enums.city import City
from unittest.mock import MagicMock, patch

VALID_PACKAGE_ID = 1
VALID_START_LOCATION = City.MEL
VALID_END_LOCATION = City.ADL
VALID_WEIGHT = 40.50
VALID_CONTACT_INFO = "pesho@gmail.com"

PACKAGE = Package()
class Initializer_Should(unittest.TestCase):
    pass