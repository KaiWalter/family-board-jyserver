import os

# general

CALENDAR_TIMEZONE = os.getenv("CALENDAR_TIMEZONE") or "UTC"


# setting specific for MS Graph (Calendar + OneDrive)

MSG_CLIENT_ID = os.getenv("MSG_CLIENT_ID")
if not MSG_CLIENT_ID:
    raise ValueError("Need to define MSG_CLIENT_ID environment variable")

MSG_CLIENT_SECRET = os.getenv("MSG_CLIENT_SECRET")
if not MSG_CLIENT_SECRET:
    raise ValueError("Need to define MSG_CLIENT_SECRET environment variable")

MSG_AUTHORITY = os.getenv("MSG_AUTHORITY")
if not MSG_AUTHORITY:
    raise ValueError("Need to define MSG_AUTHORITY environment variable")

MSG_REDIRECT_PATH = "/msgtoken"
MSG_CACHE_FILE = "msg_token.json"
MSG_ENDPOINT_CALENDAR = 'https://graph.microsoft.com/v1.0/me/calendars'
MSG_ENDPOINT_IMAGES = 'https://graph.microsoft.com/v1.0/me/drive/root:/FamilyCalendarImages:/children?$top=999'
MSG_SCOPE = ["Calendars.Read", "Files.Read.All"]
MSG_CALENDAR_PATTERN = os.getenv(
    "MSG_CALENDAR_PATTERN") or "^(Calendar|Birthdays)$"
MSG_LOCALE = os.getenv("MSG_LOCALE") or 'en_US.utf8'

# setting specific for Google Calendar

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
if not GOOGLE_CLIENT_ID:
    raise ValueError("Need to define GOOGLE_CLIENT_ID environment variable")

GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
if not GOOGLE_CLIENT_SECRET:
    raise ValueError(
        "Need to define GOOGLE_CLIENT_SECRET environment variable")

GOOGLE_REDIRECT_PATH = "/googletoken"
GOOGLE_CACHE_FILE = "google_token.pickle"
GOOGLE_SCOPE = ["https://www.googleapis.com/auth/calendar.readonly"]
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# setting specific for German Holiday calendars

GERMAN_STATE = "BW"


