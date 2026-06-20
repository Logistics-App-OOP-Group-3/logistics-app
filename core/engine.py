from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.command_factory import CommandFactory

class Engine:
    def __init__(self, factory: CommandFactory):
        self._command_factory = factory
        
    def start(self):
        output = []
        while True:
            try:
                input_line = input()
                if input_line.lower() in ['end', 'exit']:
                    break
                
                command = self._command_factory.create(input_line)
                output.append(command.execute())
            except ValueError as err:
                output.append(err[0])
                
        print('\n'.join(output))