from flask import session


def session_dump():
    session_data = ""

    for key, value in session.items():
        session_data = session_data + str(key) + ": " + str(value) + "<br>"

    return str(session_data)


def is_user_admin():
    if ("user_level" in session) and (session["user_level"] >= 100):
        return True
    else:
        return False

