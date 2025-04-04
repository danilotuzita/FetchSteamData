import os

OPEN_TAIKO_LOG_PATH = os.getenv('OPEN_TAIKO_LOG_PATH', "%LOCALAPPDATA%/OpenTaiko Hub/OpenTaiko/OpenTaiko.log")
OPEN_TAIKO_APP_ID = int(os.getenv('OPEN_TAIKO_APP_ID', "-1"))
OPEN_TAIKO_GAME_NAME = os.getenv('OPEN_TAIKO_GAME_NAME', "Open Taiko")
