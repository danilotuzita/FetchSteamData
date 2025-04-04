from dataclasses import dataclass, field
from datetime import datetime
import logging
import os
import re

from app.api.opentaiko.consts import OPEN_TAIKO_LOG_PATH


@dataclass
class TaikoSession:
    start_time: datetime = None
    end_time: datetime = None
    songs_played: list[str] = field(default_factory=list)
    _last_time: datetime = None


class GetTaikoPlaySession():
    search_str = r"^(?P<time>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(?P<level>.+)\] (?P<message>.+)$"
    matcher = re.compile(search_str)

    @staticmethod
    def get_play_session() -> TaikoSession:
        log_file_path = GetTaikoPlaySession.sanitize_log_path(OPEN_TAIKO_LOG_PATH)
        with open(log_file_path, mode='r', encoding='utf-8') as log_file:
            taiko_session = TaikoSession()
            for log in log_file:
                taiko_session = GetTaikoPlaySession.process_log(log, taiko_session)
        if not taiko_session.end_time:
            logging.warning(f"Couldn't find Open Taiko end time! Maybe it crashed? Using the last time of log={log_file_path}")
            taiko_session.end_time = taiko_session._last_time

        if not taiko_session.start_time:
            logging.error(f"Couldn't find Open Taiko start time! log={log_file_path}")
            return None

        if taiko_session.start_time > taiko_session.end_time:
            logging.error(f"Start Time is after End Time!!! What happened?? log={log_file_path}")
            return None
        return taiko_session

    @staticmethod
    def process_log(log: str, taiko_session: TaikoSession) -> TaikoSession:
        match = GetTaikoPlaySession.matcher.match(log)
        if not match:
            return taiko_session

        level = match.group('level')
        if level != "INFO":
            return taiko_session

        time = datetime.fromisoformat(match.group('time').replace("/", "-"))
        message = match.group('message')
        taiko_session._last_time = time
        if message == "Initializing skin...":
            taiko_session.start_time = time
            return taiko_session
        if message == "OpenTaiko has closed down successfully.":
            taiko_session.end_time = time
            return taiko_session
        if message.startswith("TITLE: "):
            taiko_session.songs_played.append(message.replace("TITLE: ", ""))
            return taiko_session
        return taiko_session

    @staticmethod
    def sanitize_log_path(log_path: str) -> str:
        real_log_path = os.path.expandvars(log_path)
        if not os.path.exists(real_log_path):
            raise FileNotFoundError(f"Open Taiko log file not found: {real_log_path}")
        return real_log_path
