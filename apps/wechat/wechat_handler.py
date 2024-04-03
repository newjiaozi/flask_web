import datetime
import hashlib
from flask import current_app

TOKEN = "NUONUO"  # 这个token要与我在微信公众号上设置的token是一样的


def check_sign():
    now = datetime.datetime.now()
    print(now)
    return now


def check_signature(signature, timestamp, nonce):
    token = "NUONUO"  # 修改为你在微信公众号后台设置的token字段
    # 1.将token、timestamp、nonce三个参数进行字典序排序
    s = sorted([timestamp, nonce, token])
    s = ''.join(s)
    # 2.将三个参数字符串拼接成一个字符串进行sha1加密
    hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
    # 3.开发者获得加密后的字符串可与signature对比
    if hashcode == signature:
        return True
    else:
        return False


def check_in(request):
    """
    响应微信的get请求，微信的验证信息会使用get请求
    这里的验证方式是按照微信公众号文档上的教程来做的
    :return:
    """
    # 微信传来的签名，需要和我生成的签名进行比对
    signature_str = request.args.get('signature')  # 微信已经加密好的签名，供我比对用
    timestamp = request.args.get('timestamp')  # 这是我需要的加密信息
    nonce = request.args.get('nonce')  # 也是需要的加密信息
    # 判断该请求是否正常，签名是否匹配
    try:
        # 微信传来的签名与我加密的签名进行比对，成功则返回指定数据给微信
        if check_signature(signature_str, timestamp, nonce):
            # 微信要求比对成功后返回他传来的echost数据给他
            return request.args.get('echostr')
        else:
            return ""
    except Exception:
        current_app.logger.error("签名失败！")
    return "签名失败！"


def handle_request(request):
    """
    """
    if request.method == "GET":  # 验证微信接入
        return check_in(request)
    elif request.method == "POST":  # 业务逻辑
        pass
