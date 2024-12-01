import os
from dotenv import load_dotenv  # noqa
load_dotenv()  # noqa

import logging  # noqa
logging.basicConfig(
    filename=os.getenv('LOG_NAME', "fetch_steam_data.log"),
    format=os.getenv('LOG_FORMAT', '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'),
    level=os.getenv('LOG_LEVEL', 'INFO').upper()
)
