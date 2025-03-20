from dataclasses import dataclass, field
from datetime import datetime
import logging
from os import path
import re


@dataclass
class TaikoSession:
    start_time: datetime = None
    end_time: datetime = None
    songs_played: list[str] = field(default_factory=list)
    _last_time: datetime = None


class GetTaikoPlaySession():
    local_data_dir = path.expandvars(r"%LOCALAPPDATA%") + "/"
    open_taiko_dir = "OpenTaiko Hub/OpenTaiko/"
    open_taiko_log_name = "OpenTaiko.log"

    search_str = r"^(?P<time>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(?P<level>.+)\] (?P<message>.+)$"
    matcher = re.compile(search_str)

    @staticmethod
    def get_play_session() -> TaikoSession:
        log_file_path = GetTaikoPlaySession.local_data_dir + GetTaikoPlaySession.open_taiko_dir + GetTaikoPlaySession.open_taiko_log_name
        log_file_path = log_file_path.replace("\\", "/")
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
        time = datetime.fromisoformat(match.group('time').replace("/", "-"))
        level = match.group('level')
        message = match.group('message')

        if level != "INFO":
            return taiko_session
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
