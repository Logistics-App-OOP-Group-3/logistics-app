from os import path
class DatabaseService:

    _DATA_DIR = path.join(path.dirname(__file__), '..', "data")
    _DB_FILES = {
    'vehicles': path.join(_DATA_DIR, 'vehicles.csv')
    }
    
    def __init__(self):
        self._validate_files_exist(self._DB_FILES)
        
    def read_lines(self, model_key: str):
          if model_key not in self._DB_FILES:
              raise ValueError(f"Model key: {model_key} not supported by the database.")
          with open(self._DB_FILES[model_key], 'r') as vehicles_csv:
              for line in vehicles_csv:
                  yield line.strip()
        
    @staticmethod
    def _validate_files_exist(paths: dict[str, str]):
        for key, value in paths.items():
            if not value:
                raise ValueError("File path cannot be None or empty !")
            if not path.exists(value):
                raise ValueError(f"[{key}] File does not exist !\n  At:{value}")
        