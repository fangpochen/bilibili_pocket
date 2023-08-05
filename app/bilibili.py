import datetime
import json
import logging

import requests
from flask import request
from flask_appbuilder import BaseView, expose, has_access, ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Phone, Pocket


class PocketModelView(ModelView):
    datamodel = SQLAInterface(Pocket)
    label_columns = {'price': '价值', 'room_id': '房间号', 'total_p': '在线人数', 'leave_time': '剩余秒数',
                     'update_time': '更新时间'}
    list_columns = ["id", "price", "room_id", "total_p", "leave_time", "update_time"]
    add_columns = ["id", "price", "room_id", "total_p", "leave_time", "update_time"]
    edit_columns = ["id", "price", "room_id", "total_p", "leave_time", "update_time"]
    base_order = ("update_time", "asc")


class PhoneModelView(ModelView):
    datamodel = SQLAInterface(Phone)
    label_columns = {'phone': '手机号', 'url': '请求url地址', 'state': '状态[0未使用，1已使用]', 'update_time': '更新时间',
                     'end_time': '结束时间'}
    list_columns = ["id", "phone", "url", "state", "update_time", "end_time"]
    add_columns = ["id", "phone", "url", "state", "update_time", "end_time"]
    edit_columns = ["id", "phone", "url", "state", "update_time", "end_time"]
    base_order = ("update_time", "asc")


class MyView(BaseView):
    default_view = "method1"

    @expose("/contribution/", methods=["POST"])
    @has_access
    def method1(self):
        return "Hello"

    @expose("/pocket/", methods=["GET"])
    @has_access
    def pocket(self, *args):
        now_time = datetime.datetime.now()
        pocket = db.session.query(Pocket).filter(now_time < Pocket.end_time).all()
        return pocket

    @expose("/phone/", methods=["GET"])
    @has_access
    def get_phone(self):
        now_time = datetime.datetime.now()
        phone = db.session.query(Phone).filter(Phone.state == 0, now_time < Phone.end_time).first()
        phone.state = 1
        phone.update_time = now_time
        print(phone.phone)
        db.session.commit()
        return phone.phone

    @expose("/phonesms/", methods=["GET"])
    @has_access
    def phonesms(self, *args):
        params = request.get_json()
        phone = request.args.get('phone')
        return get_bilibili_sms(phone)


def get_sms(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data


def get_bilibili_sms(phone_num):
    try:
        phone = db.session.query(Phone).filter(Phone.phone == phone_num).first()
        data = get_sms(phone.url)
        for i in data:
            content = i['content']
            if phone_num[-4:] == i['simnum'][-4:]:
                if "验证码" in content:
                    return content[9:15]
    except Exception as err:
        logging.Logger.info(err)
    return ''


appbuilder.add_view(MyView(), "Method1", category="My View")
# appbuilder.add_link("Method2", href="/myview/method2/", category="My View")
# appbuilder.add_link("Method3", href="/myview/method3/jonh", category="My View")

db.create_all()
appbuilder.add_view(
    PhoneModelView,
    "手机号",
    icon="fa-folder-open-o",
    category="phone",
    category_icon="fa-envelope"
)
appbuilder.add_view(
    PocketModelView,
    "红包",
    icon="fa-folder-open-o",
    category="pocket",
    category_icon="fa-envelope"
)

appbuilder.add_separator("phone")
appbuilder.add_separator("pocket")
