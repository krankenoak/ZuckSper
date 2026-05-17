import logging
import mood

# CONFIG
TOKEN_FILE = "token"

HAU_ID = 1
ZUCKPROSINY_ID = 1

# GLOBAL STATE
STATE = {
    "active": True,
    "mood": mood.Mood(),
    "users": {},
}

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

# STUFF
LAST_BOT_MESSAGE = {}
