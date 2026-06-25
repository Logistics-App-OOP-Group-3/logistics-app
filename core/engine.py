from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.command_factory import CommandFactory

class Engine:
    def __init__(self, factory):
        self._command_factory = factory

    def start(self):
        while True:
            try:
                input_line = input()

                if input_line.lower() in ["end", "exit"]:
                    break

                command = self._command_factory.create(input_line)
                result = command.execute()

                print(result)

            except ValueError as err:
                print(str(err))