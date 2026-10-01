from .schedules import Schedules
from .schedule_import import ScheduleImport


class Scheduling:

    def __init__(self, access_token, server_url):
        self.schedules = Schedules(access_token, server_url)
        self.schedule_import = ScheduleImport(access_token, server_url)
