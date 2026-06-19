
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING # import for type anotaion
if TYPE_CHECKING:
    from core.application_data import ApplicationData
    
    
# The idead here is to make sure Pythor will raise error
# if we dont override execute in children 
class BaseCommand(ABC):
    def __init__(self, params: list[str], app_data: ApplicationData):
        self._params = params
        self._app_data = app_data
        
    @property
    def params(self):
        return tuple(self._params)
    
    @property
    def app_data(self):
        return self._app_data
    
    @abstractmethod
    def execute(self) -> str: ...