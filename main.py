from core.application_data import ApplicationData
from core.system_report import SystemReport
from core.command_factory import CommandFactory
from core.engine import Engine

app_data = ApplicationData()
# system_report = SystemReport(app_data)
# print(system_report.info_vehicle_storage())
cmd_factory = CommandFactory()
engine = Engine()

engine.start()