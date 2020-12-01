#  Reference: https://realpython.com/primer-on-python-decorators/

import functools
from flask import Flask, redirect, session, url_for, flash, current_app as app

# https://stackoverflow.com/questions/15122312/how-to-import-from-config-file-in-flask


def session_required(func):
    """Make sure user is logged in before proceeding"""
    @functools.wraps(func)
    def session_required(*args, **kwargs):
        if session.get("user_id") is None:
            flash(u'Login required', 'alert-danger')
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return session_required


def admin_required(func):
    """Make sure user is Admin level before proceeding"""
    @functools.wraps(func)
    def admin_required(*args, **kwargs):
        if (session.get("user_level")) is None or int(session.get("user_level") < 200):
            flash(u'Admin level required', 'alert-danger')
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return admin_required


def super_admin_required(func):
    """Make sure user is Admin level before proceeding"""
    @functools.wraps(func)
    def super_admin_required(*args, **kwargs):
        if (session.get("user_level")) is None or int(session.get("user_level") < 300):
            flash(u'Super Admin level required', 'alert-danger')
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return super_admin_required


def session_required_obj(func):
    # unused
    pass

    # """Make sure user is logged in before proceeding.  Depends on config setting."""
    # @functools.wraps(func)
    # def session_required_obj(*args, **kwargs):
    #     if app.config['REQUIRE_REG_FOR_NEW_ITEMS'] == 1:
    #         if session.get("user_id") is None:
    #             return redirect(url_for("login"))
    #     return func(*args, **kwargs)
    # return session_required_obj


