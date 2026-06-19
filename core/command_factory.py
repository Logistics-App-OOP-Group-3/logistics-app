
#TODO: Import command classes


from typing import TYPE_CHECKING
# TYPE_CHECKING is bool var - used for importing for annotation purposes
# True: during code static parsing
# False: during program execution
if TYPE_CHECKING:
    from core.application_data import ApplicationData

class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data
        
        
    def create(self, input_line:str):
        cmd, *params = input_line.split()
        
        #TODO: Add command creation (new instance of custom class)
        if cmd.lower() == "":
            pass
        if cmd.lower() == "":
            pass
    
        # TODO: uncomment raise of invalid command when commands are added
        # raise ValueError(f"Invalid command name: {cmd}!")
    