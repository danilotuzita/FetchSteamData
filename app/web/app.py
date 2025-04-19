from typing import Sequence
from flask import Flask, render_template, request, redirect, url_for

from app.api.opentaiko.consts import OPEN_TAIKO_APP_ID
from app.repository.view.play_session_view import PlaySessionView
from app.service.play_session_service import PlaySessionService

app = Flask(__name__)


@app.route('/')
def index():
    sessions = PlaySessionService.get_latest_play_sessions()  # Fetch play sessions from your service
    return render_template('index.html', sessions_by_date=break_by_date(sessions))


@app.route('/play-sessions')
def play_sessions():
    sessions = PlaySessionService.get_latest_play_sessions()  # Fetch play sessions from your service
    return render_template('play_sessions.html', sessions=sessions)


@app.route('/execute', methods=['POST'])
def execute_operation():
    operation = request.form.get('operation')
    # Call your application's logic here
    # result = PlaySessionService.execute_operation(operation)
    return redirect(url_for('index'))


def break_by_date(sessions: Sequence[PlaySessionView]) -> dict[str, list[PlaySessionView]]:
    result: dict[str, list[PlaySessionView]] = {}
    for session in sessions:
        cover_art_url = ""
        if session.appid == OPEN_TAIKO_APP_ID:
            cover_art_url = "/static/OpenTaiko.jpg"
        else:
            cover_art_url = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{session.appid}/header.jpg"
        session.cover_art = cover_art_url
        # session.cover_art = f"background-image: url('{cover_art_url}');"
        result.setdefault(session.session_time[:10], []).insert(0, session)
    return result
