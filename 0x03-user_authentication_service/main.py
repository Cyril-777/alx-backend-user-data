#!/usr/bin/env python3
"""
Main file
"""

import requests


def register_user(email: str, password: str) -> None:
    """Register user"""
    r = requests.post('http://localhost:5000/users', data={
        'email': email,
        'password': password
    })
    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password"""
    r = requests.post('http://localhost:5000/sessions', data={
        'email': email,
        'password': password
    })
    assert r.status_code == 401


def profile_unlogged() -> None:
    """Profile of unlogged user"""
    r = requests.get('http://localhost:5000/profile')
    assert r.status_code == 403


def log_in(email: str, password: str) -> str:
    """Log in"""
    r = requests.post('http://localhost:5000/sessions', data={
        'email': email,
        'password': password
    })
    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'logged in'}
    return r.cookies.get('session_id', None)


def profile_logged(session_id: str) -> None:
    """Profile of logged user"""
    r = requests.get('http://localhost:5000/profile', cookies={
        'session_id': session_id
    })
    assert r.status_code == 200
    assert r.json() == {'email': email}


def log_out(session_id: str) -> None:
    """Log out"""
    r = requests.delete('http://localhost:5000/sessions', cookies={
        'session_id': session_id
    })
    assert r.status_code == 200
    assert r.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    """Reset password token"""
    r = requests.post('http://localhost:5000/reset_password', data={
        'email': email
    })
    assert r.status_code == 200
    assert len(r.text) == 36
    return r.text


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    r = requests.put('http://localhost:5000/reset_password', data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })
    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
