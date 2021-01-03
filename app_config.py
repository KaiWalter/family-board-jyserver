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

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/me/calendars'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["Calendars.Read","Files.Read.All"]

CALENDAR_PATTERN="^(us|Calendar)"
CALENDAR_TIMEZONE="Europe/Berlin"

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

CACHE_FILE = "server_cache.bin"

LOCALE = 'en_US.utf8'