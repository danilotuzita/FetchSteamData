# FetchSteamData

Create a `.env` file in the root of the project with the following configuration:
``` ini
# USER KEYS
STEAM_API_KEY=<YOUR STEAM KEY API>
STEAM_ID_64=<YOUR STEAM 64BIT ID>
```
You also can also set the following enviroment variables:
VARIABLE        | DESCRIPTION                   | DEFAULT
----------------|-------------------------------|--------------------------------------------------------------------------------
`LOG_NAME`      | Log file name                 | `fetch_steam_data.log`
`LOG_LEVEL`     | Log level                     | `INFO`
`LOG_FORMAT`    | Log format                    | `%(asctime)s,%(msecs)03d %(levelname)-5s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s`
`LOG_TO_CONSOLE`| Toggle logging to console too | `False`
`DATABASE_NAME` | Name for the SQLite db file   | `steam.db`


Run `main.py`
