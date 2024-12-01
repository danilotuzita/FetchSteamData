import config
from app.service.steam_service import SteamService

if __name__ == "__main__":
    SteamService.fetch_user_data_from_steam_api_and_save_to_db()
