from os import path, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable
    
    
class FileService:
    """ 
    Current database is a file system.
    The class provides generic way to read/write different files with 
        write_lines
        read_lines
    functions via: _MAP_MODEL_KEY_TO_FILE.
    """

    _FILE_DIR = path.join(path.dirname(__file__), '..', "data")
    _MAP_MODEL_KEY_TO_FILE = {
    'vehicles': path.join(_FILE_DIR, 'vehicles.csv')
    }
    
    
    def __init__(self):
        self._validate_files_exist(self._MAP_MODEL_KEY_TO_FILE)
        
        
    def write_lines(self, model_key: str, lines: Iterable[str]) :
        """Write to file matching param[0]: model_key line by line
        lazily with generator passed to param[1]: lines
        Create tmp file and after writing is finished, replace the old one"""
        
        self._validate_model_key(model_key)
        path = self._MAP_MODEL_KEY_TO_FILE[model_key]
        tmp = path.replace('.csv', '_tmp.csv') # str.replace
        
        with open(tmp, 'w') as write_file:
            for line in lines:
                write_file.write(line + '\n')
        
        replace(tmp, path)  # os.replace
        
        
    def read_lines(self, model_key: str):
        """ Read files line by line and return values lazily with generator """
        
        self._validate_model_key(model_key)
        path = self._MAP_MODEL_KEY_TO_FILE[model_key]
        
        with open(path, 'r') as vehicles_csv:
            for line in vehicles_csv:
                stripped = line.strip()
                if stripped:
                    yield stripped
    
    
    #TODO: add enum for validation  
    def _validate_model_key(self, value: str):
        if value not in self._MAP_MODEL_KEY_TO_FILE:
            raise ValueError(f"Model key: {value} not supported by the database.")
            
    @staticmethod
    def _validate_files_exist(paths: dict[str, str]):
        for key, value in paths.items():
            if not value:
                raise ValueError("File path cannot be None or empty !")
            if not path.exists(value):
                raise ValueError(f"[{key}] File does not exist !\n  At:{value}")
        