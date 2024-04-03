from flask import Blueprint
from apps.test.test_handler import *

blueprint_test = Blueprint(name="test", import_name="__name__", url_prefix="/test")


@blueprint_test.route('/')
def who_am_i():
    return "Flask Web"


@blueprint_test.route('/hello/<name>')
def hello_name(name):
    return f"Flask Web {name}"


@blueprint_test.route('/time')
def hello_time():
    return f"Flask Web {get_now()}"


