import os
import json
import logging

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = logging.getLevelName(os.getenv("LOGGING_LEVEL", 'INFO'))

NETSUITE_HOST = os.getenv("NETSUITE_HOST")
NETSUITE_CREDENTIALS = {
    "consumer_key": os.getenv("NETSUITE_CONSUMER_KEY"),
    "consumer_secret": os.getenv("NETSUITE_CONSUMER_SECRET"),
    "token_key": os.getenv("NETSUITE_TOKEN_KEY"),
    "token_secret": os.getenv("NETSUITE_TOKEN_SECRET"),
    "realm": os.getenv("NETSUITE_REALM"),
}
NETSUITE_SCRIPTS = json.loads(os.getenv("NETSUITE_SCRIPTS", "{}"))
