import json
from datetime import datetime


def save_session_to_json(user_phone, message, response):
    session_data = {
        'user_phone': user_phone,
        'message': message,
        'response': str(response),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Load existing data or initialize an empty list
    try:
        with open(f'chatbot_sessions_{user_phone}.json', 'r') as f:
            sessions = json.load(f)
    except FileNotFoundError:
        sessions = []

    # Append new session data
    sessions.append(session_data)

    # Save back to the file
    with open(f'chatbot_sessions_{user_phone}.json', 'w') as f:
        json.dump(sessions, f, indent=4)


def view_session_history(user_phone):
    try:
        with open(f'chatbot_sessions_{user_phone}.json', 'r') as f:
            sessions = json.load(f)
        for session in sessions:
            print(f"User: {session['user_phone']}, Message: {session['message']}, Response: {session['response']}, Time: {session['timestamp']}")
    except FileNotFoundError:
        print("No session history found.")


def get_last_message(user_phone):
    try:
        with open(f'chatbot_sessions_{user_phone}.json', 'r') as f:
            sessions = json.load(f)
        if sessions:
            return sessions[-1]['message']
        return ""
    except FileNotFoundError:
        print("No session history found.")
