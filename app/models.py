from datetime import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, DateTime, Float

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


# 会员
class Team(Model):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True)  # 编号
    name = Column(String(100), unique=True)  # 昵称
    number = Column(String(100))  # 号码

    def __repr__(self):
        return "<Team %r>" % self.name


# 手机号
class Phone(Model):
    __tablename__ = "phone"
    id = Column(Integer, primary_key=True)  # 编号
    phone = Column(String(100), unique=True)  # 手机号
    url = Column(String(200))  # 号码api
    state = Column(Integer)  # 状态 0 未使用 1已使用
    update_time = Column(DateTime, index=True, default=datetime.now)  # 更新时间
    end_time = Column(DateTime, index=True, default=datetime.now)  # 结束时间

    def __repr__(self):
        return "<Phone %r>" % self.name


# 红包
class Pocket(Model):
    __tablename__ = "pocket"
    id = Column(Integer, primary_key=True)  # 编号
    room_id = Column(String(200), primary_key=True)  # 房间号
    price = Column(Integer)  # 价值
    total_p = Column(Integer)  # 在线人数
    leave_time = Column(Integer)  # 剩余秒数
    update_time = Column(DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<Pocket %r>" % self.name


# 天选
class Tian(Model):
    __tablename__ = "tian"
    id = Column(Integer, primary_key=True)  # 编号
    room_id = Column(String(200), primary_key=True)  # 房间号
    price = Column(String(200))  # 价值
    total_p = Column(Integer)  # 在线人数
    leave_time = Column(Integer)  # 剩余秒数
    update_time = Column(DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<Tian %r>" % self.name


# 数据
class Data(Model):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)  # 编号
    uuid = Column(String(100), unique=True)  # 比赛uuid
    homeTeam = Column(String(100))  # 主队
    visitTeam = Column(String(100))  # 客队
    homeTeam_score = Column(Float)  # 主队得分
    visitTeam_score = Column(Float)  # 客队得分
    homeTeam_half = Column(Float)  # 主队半场
    visitTeam_half = Column(Float)  # 客队半场
    dish = Column(Float)  # pankou
    size = Column(Float)
    result_dish = Column(Integer)
    result_home = Column(Integer)
    result_size = Column(Integer)
    play_time = Column(DateTime, index=True, default=datetime.now)  # 比赛时间

    def __repr__(self):
        return "<Data %r>" % self.id


# 标签
class Dish_Data(Model):
    __tablename__ = "dish_data"
    id = Column(Integer, primary_key=True)  # 编号
    his_continuous_on_day = Column(Integer)  # 历史强队连续最高天数
    his_continuous_down_day = Column(Integer)  # 历史弱队连续最高天数
    his_continuous_on = Column(Integer)  # 历史强队连续最高场数
    his_continuous_down = Column(Integer)  # 历史弱队连续最高场数
    on_number = Column(Integer)  # 上盘总数量
    down_number = Column(Integer)  # 下盘总数量
    total_deviation = Column(Integer)  # 历史数据的总偏差值
    total = Column(Integer)  # 历史数据总数
    current_continuous_day = Column(Integer)  # 当前连续方向天数
    current_continuous = Column(Integer)  # 当前连续方向场数
    now_day = Column(Integer)  # 当天总偏差值
    two_day = Column(Integer)  # 2天总偏差值
    three_day = Column(Integer)  # 3天前连续偏差值
    update_time = Column(DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<Dish_Data %r>" % self.id


# 标签
class Home_Data(Model):
    __tablename__ = "home_data"
    id = Column(Integer, primary_key=True)  # 编号
    his_continuous_home_day = Column(Integer)  # 历史主队连续最高天数
    his_continuous_visit_day = Column(Integer)  # 历史客队连续最高天数
    his_continuous_home = Column(Integer)  # 历史主队连续最高场数
    his_continuous_visit = Column(Integer)  # 历史客队连续最高场数
    home_number = Column(Integer)  # 主场盘总数量
    visit_number = Column(Integer)  # 客场盘总数量
    total_deviation = Column(Integer)  # 历史数据的总偏差值
    total = Column(Integer)  # 历史数据总数
    current_continuous_day = Column(Integer)  # 当前连续方向天数
    current_continuous = Column(Integer)  # 当前连续方向场数
    now_day = Column(Integer)  # 当天总偏差值
    two_day = Column(Integer)  # 2天总偏差值
    three_day = Column(Integer)  # 3天前连续偏差值
    update_time = Column(DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<Home_Data %r>" % self.id


class Size_Data(Model):
    __tablename__ = "size_data"
    id = Column(Integer, primary_key=True)  # 编号
    his_continuous_big_day = Column(Integer)  # 历史大分分连续最高天数
    his_continuous_small_day = Column(Integer)  # 历史小分连续最高天数
    his_continuous_big = Column(Integer)  # 历史大分连续最高场数
    his_continuous_small = Column(Integer)  # 历史小分连续最高场数
    big_number = Column(Integer)  # 大分总数量
    small_number = Column(Integer)  # 小分总数量
    total_deviation = Column(Integer)  # 历史数据的总偏差值
    total = Column(Integer)  # 历史数据总数
    current_continuous_day = Column(Integer)  # 当前连续方向天数
    current_continuous = Column(Integer)  # 当前连续方向场数
    now_day = Column(Integer)  # 当天总偏差值
    two_day = Column(Integer)  # 2天总偏差值
    three_day = Column(Integer)  # 3天前连续偏差值
    update_time = Column(DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<Size_Data %r>" % self.id


class Premier_League(Model):
    __tablename__ = "premier_league"
    id = Column(Integer, primary_key=True)  # 编号
    snai = Column(Float)  # 主胜赔率
    lb = Column(Float)  # 主胜赔率
    wlxe = Column(Float)  # 主胜赔率
    crown = Column(Float)  # 主胜赔率
    ysb = Column(Float)  # 主胜赔率
    am = Column(Float)  # 主胜赔率
    wd = Column(Float)  # 主胜赔率
    bet365 = Column(Float)  # 主胜赔率
    result = Column(Integer)  # 结果
    number = Column(Integer, unique=True)  # 编号

    def __repr__(self):
        return "<Premier_League %r>" % self.id
