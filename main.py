from app.repository.database_repository import DatabaseRepository
import config
from app.service.steam_service import SteamService

if __name__ == "__main__":
    # print(DatabaseRepository.get_app_achivements_count(203140))
    # SteamService.fetch_data_from_steam_api_and_save_to_db()
    SteamService.do_things()
