class BaseCalendarEntry:
    def __init__(self, description:str, date:str, is_primary:bool):
        self.description = description
        self.date = date
        self.time = ""
        self.is_primary = is_primary
        self.all_day = False
        self.public_holiday = False
        self.school_holiday = False

class CalendarEntry(BaseCalendarEntry):
    def __init__(self, description:str, date:str, time:str, is_primary:bool):
        super().__init__(description, date, is_primary)
        self.time = time

class AllDayCalendarEntry(BaseCalendarEntry):
    def __init__(self, description:str, date:str, is_primary:bool):
        super().__init__(description, date, is_primary)
        self.all_day = True

class PublicHolidayDayCalendarEntry(AllDayCalendarEntry):
    def __init__(self, description:str, date:str):
        super().__init__(description, date, is_primary=False)
        self.public_holiday = True

class SchoolHolidayDayCalendarEntry(AllDayCalendarEntry):
    def __init__(self, description:str, date:str):
        super().__init__(description, date, is_primary=False)
        self.school_holiday = True
