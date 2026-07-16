from core.application_data import ApplicationData
# from core.system_report import SystemReport
from core.command_factory import CommandFactory
from core.engine import Engine

# Delivery management system developed to solve business challenges for a logistics company
#     (or, if you ask us, one even better than DHL or Uber).

#     For an overview of the project's functionality and use cases, refer to:
#         .\docs\use_case.md

#     The implementation is based on the original business requirements contract,
#     which is not included in this repository.
    
#     Designed and implemented by <Nikola Simove> and <Tsvetelin Istatkov>.


 
app_data = ApplicationData()
cmd_factory = CommandFactory(app_data)
engine = Engine(cmd_factory)
engine.start()


