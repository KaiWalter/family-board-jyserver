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

REDIRECT_PATH = "/msatoken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

ENDPOINT_CALENDAR = 'https://graph.microsoft.com/v1.0/me/calendars'
ENDPOINT_IMAGES = 'https://graph.microsoft.com/v1.0/me/drive/root:/FamilyCalendarImages:/children?$top=999'

SCOPE = ["Calendars.Read","Files.Read.All"]

CALENDAR_PATTERN="^(us|Calendar)"
CALENDAR_TIMEZONE="Europe/Berlin"

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

CACHE_FILE = "server_cache.bin"

LOCALE = os.getenv("LOCALE")
if not LOCALE:
    LOCALE = 'en_US.utf8'