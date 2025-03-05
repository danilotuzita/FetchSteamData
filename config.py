import os
import sys
from dotenv import load_dotenv  # noqa
load_dotenv()  # noqa

import logging  # noqa
logging.basicConfig(
    filename=os.getenv('LOG_NAME', "fetch_steam_data.log"),
    format=os.getenv('LOG_FORMAT', '%(asctime)s %(levelname)-5s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'),
    level=os.getenv('LOG_LEVEL', 'INFO').upper()
)
logging.addLevelName(logging.WARNING, 'WARN')

if bool(os.getenv('LOG_TO_CONSOLE', False)):
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
