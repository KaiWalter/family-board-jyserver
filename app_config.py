import os

CLIENT_ID = os.getenv("CLIENT_ID")
if not CLIENT_ID:
    raise ValueError("Need to define CLIENT_ID environment variable")

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not CLIENT_SECRET:
    raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = os.getenv("AUTHORITY")
if not AUTHORITY:
    raise ValueError("Need to define AUTHORITY environment variable")

REDIRECT_PATH = "/msatoken"
ENDPOINT_CALENDAR = 'https://graph.microsoft.com/v1.0/me/calendars'
ENDPOINT_IMAGES = 'https://graph.microsoft.com/v1.0/me/drive/root:/FamilyCalendarImages:/children?$top=999'

SCOPE = ["Calendars.Read", "Files.Read.All"]

SESSION_TYPE = "filesystem"
CACHE_FILE = "server_cache.bin"

CALENDAR_PATTERN = os.getenv("CALENDAR_PATTERN") or "^(Calendar|Birthdays)$"
CALENDAR_TIMEZONE = os.getenv("CALENDAR_TIMEZONE") or "UTC"
LOCALE = os.getenv("LOCALE") or 'en_US.utf8'
