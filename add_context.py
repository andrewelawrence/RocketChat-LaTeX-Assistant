import sys, os
from llmproxy import pdf_upload
from logger_config import get_logger

_LOGGER = get_logger(__name__)
_LOGGER.info("Add Context Begun.")

if len(sys.argv) < 2:
    print("Usage: python script.py <pdf filepath> [<pdf filepath>]")
    sys.exit(1)

for file_path in sys.argv[1:]:
    desc = os.path.basename(file_path)
    response = pdf_upload(path = file_path,
                          description = desc,
                          session_id = 'hw04')
    _LOGGER.info(f"Response for {desc}: {response}")
