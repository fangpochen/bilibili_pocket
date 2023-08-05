import requests
from flask import render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Team, Data, Dish_Data, Home_Data, Size_Data, Premier_League
from .util import get_data

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


class DataModelView(ModelView):
    datamodel = SQLAInterface(Data)
    label_columns = {'homeTeam': '主队', 'visitTeam': '客队', 'homeTeam_score': '主队得分', 'visitTeam_score': '客队得分',
                     'homeTeam_half': '主队半场得分', 'visitTeam_half': '客队半场得分', 'dish': '盘口', 'size': '客队得分',
                     'result_dish': '强弱结果', 'result_home': '主客结果', 'result_size': '大小结果', 'play_time': '比赛时间'}
    list_columns = ["id", "uuid", "homeTeam", "visitTeam", "homeTeam_score", "visitTeam_score", "homeTeam_half",
                    "visitTeam_half", "dish", "size", "result_dish", "result_home", "result_size", "play_time"]
    add_columns = ["id", "uuid", "homeTeam", "visitTeam", "homeTeam_score", "visitTeam_score", "homeTeam_half",
                   "visitTeam_half", "dish", "size", "result_dish", "result_home", "result_size", "play_time"]
    edit_columns = ["id", "uuid", "homeTeam", "visitTeam", "homeTeam_score", "visitTeam_score", "homeTeam_half",
                    "visitTeam_half", "dish", "size", "result_dish", "result_home", "result_size", "play_time"]
    base_order = ("play_time", "asc")

    def action_post(self):
        version = [{'1': '常规赛', '2': '季后赛', '3': '季前赛'}]
        url = 'http://nba.win007.com/jsData/matchResult/21-22/l1_3.js?version=2021101022'
        text = requests.get(url).text
        array = text.replace('\n', '').split(";")
        game = array[0]
        team = array[1]
        data = array[2]
        time = array[3]
        data = data[data.find('='):len(data)].replace('\'', '').split(']')
        team_map = TeamModelView.list()
        result = get_data(data, team_map)
        return "ok"


class TeamModelView(ModelView):
    datamodel = SQLAInterface(Team)
    add_columns = ["id", "name", "number"]


class Dish_DataModeView(ModelView):
    datamodel = SQLAInterface(Dish_Data)
    label_columns = {'his_continuous_on_day': '历史强队连续最高天数', 'his_continuous_down_day': '历史弱队连续最高天数',
                     'his_continuous_on': '历史强队连续最高场数', 'his_continuous_down': '历史弱队连续最高场数',
                     'on_number': '上盘总数量', 'down_number': '下盘总数量', 'total_deviation': '历史数据的总偏差值', 'total': '历史数据总数',
                     'current_continuous_day': '当前连续方向天数', 'current_continuous': '当前连续方向场数', 'update_time': '更新时间'}
    list_columns = ["id", "his_continuous_on_day", "his_continuous_down_day", "his_continuous_on",
                    "his_continuous_down", "on_number", "down_number",
                    "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                    "three_day", "update_time"]
    add_columns = ["id", "his_continuous_on_day", "his_continuous_down_day", "his_continuous_on",
                   "his_continuous_down", "on_number", "down_number",
                   "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                   "three_day", "update_time"]
    edit_columns = ["id", "his_continuous_on_day", "his_continuous_down_day", "his_continuous_on",
                    "his_continuous_down", "on_number", "down_number",
                    "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                    "three_day", "update_time"]
    base_order = ("update_time", "asc")


class Home_DataModeView(ModelView):
    datamodel = SQLAInterface(Home_Data)
    label_columns = {'his_continuous_home_day': '历史主队连续最高天数', 'his_continuous_visit_day': '历史客队连续最高天数',
                     'his_continuous_home': '历史主队连续最高场数', 'his_continuous_visit': '历史客队连续最高场数',
                     'home_number': '主队总数量', 'visit_number': '客队总数量', 'total_deviation': '历史数据的总偏差值', 'total': '历史数据总数',
                     'current_continuous_day': '当前连续方向天数', 'current_continuous': '当前连续方向场数', 'update_time': '更新时间'}
    list_columns = ["id", "his_continuous_home_day", "his_continuous_visit_day", "his_continuous_home",
                    "his_continuous_visit", "home_number", "visit_number",
                    "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                    "three_day", "update_time"]
    add_columns = ["id", "his_continuous_home_day", "his_continuous_visit_day", "his_continuous_home",
                   "his_continuous_visit", "home_number", "visit_number",
                   "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                   "three_day", "update_time"]
    edit_columns = ["id", "his_continuous_home_day", "his_continuous_visit_day", "his_continuous_home",
                    "his_continuous_visit", "home_number", "visit_number",
                    "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                    "three_day", "update_time"]
    base_order = ("update_time", "asc")


class Size_DataModeView(ModelView):
    datamodel = SQLAInterface(Size_Data)
    label_columns = {'his_continuous_big_day': '历史大分连续最高天数', 'his_continuous_small_day': '历史小分连续最高天数',
                     'his_continuous_big': '历史大分连续最高场数', 'his_continuous_small': '历史小分连续最高场数',
                     'big_number': '大分总数量', 'small_number': '小分总数量', 'total_deviation': '历史数据的总偏差值', 'total': '历史数据总数',
                     'current_continuous_day': '当前连续方向天数', 'current_continuous': '当前连续方向场数', 'update_time': '更新时间'}
    list_columns = ["id", "his_continuous_big_day", "his_continuous_small_day", "his_continuous_big",
                    "his_continuous_small", "big_number", "small_number",
                    "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                    "three_day", "update_time"]
    add_columns = ["id", "his_continuous_big_day", "his_continuous_small_day", "his_continuous_big",
                   "his_continuous_small", "big_number", "small_number",
                   "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                   "three_day", "update_time"]
    edit_columns = ["id", "his_continuous_big_day", "his_continuous_small_day", "his_continuous_big",
                    "his_continuous_small", "big_number", "small_number",
                    "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
                    "three_day", "update_time"]
    base_order = ("update_time", "asc")


class Premier_LeagueView(ModelView):
    datamodel = SQLAInterface(Premier_League)
    # label_columns = {'his_continuous_big_day': '历史大分连续最高天数', 'his_continuous_small_day': '历史小分连续最高天数',
    #                  'his_continuous_big': '历史大分连续最高场数', 'his_continuous_small': '历史小分连续最高场数',
    #                  'big_number': '大分总数量', 'small_number': '小分总数量', 'total_deviation': '历史数据的总偏差值', 'total': '历史数据总数',
    #                  'current_continuous_day': '当前连续方向天数', 'current_continuous': '当前连续方向场数', 'update_time': '更新时间'}
    # list_columns = ["id", "his_continuous_big_day", "his_continuous_small_day", "his_continuous_big",
    #                 "his_continuous_small", "big_number", "small_number",
    #                 "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
    #                 "three_day", "update_time"]
    # add_columns = ["id", "his_continuous_big_day", "his_continuous_small_day", "his_continuous_big",
    #                "his_continuous_small", "big_number", "small_number",
    #                "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
    #                "three_day", "update_time"]
    # edit_columns = ["id", "his_continuous_big_day", "his_continuous_small_day", "his_continuous_big",
    #                 "his_continuous_small", "big_number", "small_number",
    #                 "total_deviation", "total", "current_continuous_day", "current_continuous", "now_day", "two_day",
    #                 "three_day", "update_time"]
    # base_order = ("update_time", "asc")


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
appbuilder.add_view(
    TeamModelView,
    "球队",
    icon="fa-folder-open-o",
    category="ball",
    category_icon="fa-envelope"
)
appbuilder.add_separator("ball")
appbuilder.add_view(
    DataModelView,
    "数据",
    icon="fa-envelope",
    category="ball"
)
appbuilder.add_view(
    Dish_DataModeView,
    "强弱结果",
    icon="fa-envelope",
    category="ball"
)
appbuilder.add_view(
    Home_DataModeView,
    "主客结果",
    icon="fa-envelope",
    category="ball"
)
appbuilder.add_view(
    Size_DataModeView,
    "大小结果",
    icon="fa-envelope",
    category="ball"
)
appbuilder.add_view(
    Premier_LeagueView,
    "英超结果",
    icon="fa-envelope",
    category="ball"
)