#
# Reminder, export environment variables prior to running this function.
#
# ```bash
# $ ./load_envs.sh
# ```
#

import os, requests
from config import get_logger

# Setup logger
_LOGGER = get_logger(__name__)
_LOGGER.info("Test Process Begun.")

# Read in config
msgUrl = os.environ.get("msgUrl")
koyebUrl = os.environ.get("koyebUrl")
rcBotToken = os.environ.get("rcBotToken")
rcBotId = os.environ.get("rcUserId")
testUser = os.environ.get("testUser")
testText = open(os.environ.get("testText")).read()

# Setup http POST
headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": rcBotToken,
    "X-User-Id": rcBotId
}

payload = {
    "channel": testUser,
    "text": testText
}

# POST
resp = requests.post(koyebUrl, json=payload, headers=headers)

# Log Response
_LOGGER.info((f"Status Code: {resp.status_code}"))
_LOGGER.info((f"LLMProxy Response: {resp.text}"))
