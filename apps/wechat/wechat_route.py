from flask import Blueprint,request
from apps.wechat.wechat_handler import *

blueprint_wechat = Blueprint(name="wechat", import_name="__name__", url_prefix="/wechat")


@blueprint_wechat.route('/')
def check():
    return check_in(request)



