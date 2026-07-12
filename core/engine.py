from __future__ import annotations
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from core.command_factory import CommandFactory

class Engine:
    def __init__(self, factory: CommandFactory):
        self._command_factory = factory
        
    def start(self):
        
        self.clear_console()
        
        while True:
            try:
                input_line = input().strip()

                if input_line.lower() in ["end", "exit"]:
                    break

                command = self._command_factory.create(input_line)
                result = command.execute()

                print(result)

            except ValueError as err:
                print(str(err))
        
        self._command_factory._data_repository.save() # save data to files on exit
    
    @staticmethod
    def clear_console():
        # 'nt' - Windows, 'posix' - Linux & macOS
        os.system('cls' if os.name == 'nt' else 'clear')