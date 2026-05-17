import os
from dotenv import load_dotenv
import logging
import mood

# CONFIG
load_dotenv()

TOKEN = os.getenv("TOKEN")

HAU_ID = int(os.getenv("HAU_ID"))
ZUCKPROSINY_ID = int(os.getenv("ZUCKPROSINY_ID"))

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
