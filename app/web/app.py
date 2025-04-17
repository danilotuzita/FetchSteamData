from flask import Flask, render_template, request, redirect, url_for

from app.service.play_session_service import PlaySessionService

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
