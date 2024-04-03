import datetime
import hashlib
import time

from flask import current_app, make_response
import xml.etree.cElementTree as ET
import os

TOKEN = os.environ.get("WECHAT_TOKEN")  # 这个token要与我在微信公众号上设置的token是一样的


def check_signature(request):
    token = TOKEN  # 修改为你在微信公众号后台设置的token字段
    # 微信传来的签名，需要和我生成的签名进行比对
    try:
        # 微信传来的签名与我加密的签名进行比对，成功则返回指定数据给微信
        signature_str = request.args.get('signature')  # 微信已经加密好的签名，供我比对用
        timestamp = request.args.get('timestamp')  # 这是我需要的加密信息
        nonce = request.args.get('nonce')  # 也是需要的加密信息
        # 判断该请求是否正常，签名是否匹配
        # 1.将token、timestamp、nonce三个参数进行字典序排序
        s = sorted([timestamp, nonce, token])
        s = ''.join(s)
        # 2.将三个参数字符串拼接成一个字符串进行sha1加密
        hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        # 3.开发者获得加密后的字符串可与signature对比
        if hashcode == signature_str:
            return True
        else:
            return False  # 微信要求比对成功后返回他传来的echost数据给他
    except Exception:
        current_app.logger.error("签名失败！")
    return False


def handle_response(request):
    xml = ET.fromstring(request.data)
    to_user = xml.find('ToUserName').text
    from_user = xml.find('FromUserName').text
    msg_type = xml.find("MsgType").text
    content = xml.find("Content").text
    if msg_type == 'text':
        reply = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
                '''
        response = make_response(reply % (from_user, to_user, str(int(time.time())), content))
        response.headers['content-type'] = 'application/xml'
        return response
    elif msg_type == 'event':
        event = xml.find('Event').text
        if event == 'subscribe':  # 关注
            msg = 'welcome 输入关键字试试~~'
        else:  # 取消关注
            msg = '期待你的下次关注~'
        reply = '''<xml>
                            <ToUserName><![CDATA[%s]]></ToUserName>
                            <FromUserName><![CDATA[%s]]></FromUserName>
                            <CreateTime>%s</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[%s]]></Content>
                            </xml>'''
        response = make_response(reply % (from_user, to_user, str(int(time.time())), msg))
        response.headers['content-type'] = 'application/xml'
        return response
    else:
        reply = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
                '''
        response = make_response(reply % (from_user, to_user, str(int(time.time())), "只能识别文字哦～"))
        response.headers['content-type'] = 'application/xml'
        return response


def handle_request(request):
    """
    """
    if not check_signature(request):
        return ""
    if request.method == "GET":  # 验证微信接入
        return request.args.get('echostr')
    elif request.method == "POST":  # 业务逻辑
        return handle_response(request)
