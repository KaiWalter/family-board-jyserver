import os

# setting specific for MS Graph (Calendar + OneDrive)

MSG_CLIENT_ID = os.getenv("MSG_CLIENT_ID")
if not MSG_CLIENT_ID:
    raise ValueError("Need to define CLIENT_ID environment variable")

MSG_CLIENT_SECRET = os.getenv("MSG_CLIENT_SECRET")
if not MSG_CLIENT_SECRET:
    raise ValueError("Need to define CLIENT_SECRET environment variable")

MSG_AUTHORITY = os.getenv("MSG_AUTHORITY")
if not MSG_AUTHORITY:
    raise ValueError("Need to define AUTHORITY environment variable")

MSG_REDIRECT_PATH = "/msatoken"
MSG_ENDPOINT_CALENDAR = 'https://graph.microsoft.com/v1.0/me/calendars'
MSG_ENDPOINT_IMAGES = 'https://graph.microsoft.com/v1.0/me/drive/root:/FamilyCalendarImages:/children?$top=999'
MSG_SCOPE = ["Calendars.Read", "Files.Read.All"]
MSG_CALENDAR_PATTERN = os.getenv("MSG_CALENDAR_PATTERN") or "^(Calendar|Birthdays)$"
MSG_CALENDAR_TIMEZONE = os.getenv("MSG_CALENDAR_TIMEZONE") or "UTC"
MSG_LOCALE = os.getenv("MSG_LOCALE") or 'en_US.utf8'

# setting specific for German Holiday calendars

GERMAN_STATE = "BW"

# Flask cache settings

SESSION_TYPE = "filesystem"
CACHE_FILE = "server_cache.bin"
