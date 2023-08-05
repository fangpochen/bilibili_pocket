import datetime
import random

import numpy as np
from app import db

from app.models import Team, Data


def get_team_name(team):
    team_array = []
    for i in team:
        try:
            i = i.replace(',[', '').replace('[', '').replace('=', '').replace(' ', '')
            result = i.split(',')
            team_array.append(Team(id=result[0], name=result[1]))
        except:
            break
    return team_array


def get_data(data, team_map):
    result = []
    for i in data:
        try:
            i = i[i.find(':') - 13:-1]
            n = i.split(',')

            homeTeam = team_map[int(n[1]) - 1].name
            visitTeam = team_map[int(n[2]) - 1].name
            homeTeam_score = float(n[3])
            visitTeam_score = float(n[4])
            homeTeam_half = float(n[5])
            visitTeam_half = float(n[6])
            dish = float(n[8])
            size = float(n[9])
            uuid = homeTeam + visitTeam + ' ' + n[0]
            play_time = datetime.datetime.strptime(str(n[0]), "%Y-%m-%d %H:%M")
            if dish > 0:
                if homeTeam_score > visitTeam_score + dish:
                    result_dish = 1  # 上
                else:
                    result_dish = -1  # 下
            else:
                if homeTeam_score < visitTeam_score + dish:
                    result_dish = 1  # 上
                else:
                    result_dish = -1  # 下
            if homeTeam_score > visitTeam_score + dish:
                result_home = 1  # 主
            else:
                result_home = -1  # 客
            if homeTeam_score + visitTeam_score > size:
                result_size = 1  # 大
            else:
                result_size = -1  # 小

            # data_resu.update({})
            model = Data(uuid=uuid,
                         homeTeam=homeTeam,
                         visitTeam=visitTeam,
                         homeTeam_score=homeTeam_score,
                         visitTeam_score=visitTeam_score,
                         homeTeam_half=homeTeam_half,
                         visitTeam_half=visitTeam_half,
                         dish=dish,
                         size=size,
                         result_dish=result_dish,
                         result_home=result_home,
                         result_size=result_size,
                         play_time=play_time)
            result.append(model)
        except Exception as e:
            print(i)
            print(e)
            continue
    return result


def total_data(list, label):
    total = 0
    for i in list:
        n = i.__getattribute__(label)
        total = total + n
    return total


def max_num(list, label):
    old_num = 0
    max_num_on = 0
    max_num_down = 0
    total_on = 0
    total_down = 0
    tmp = 0
    for i in list:
        n = i.__getattribute__(label)
        if n > 0:
            total_on = total_on + n
        else:
            total_down = total_down + n
        ##计算连续次数
        if old_num != n:
            old_num = n
            tmp = 0
        else:
            tmp = tmp + n
        if max_num_on < tmp:
            max_num_on = tmp
            # print('在过去的时间里', i.play_time, 'max_num')
            # print(tmp, 'max_num')
        if max_num_down > tmp:
            max_num_down = tmp
            # print(tmp)
            # print(i.play_time)
    return max_num_on, max_num_down, tmp, total_on, total_down


def max_day(list, label):
    old_day = ''
    tmp = 0
    array = []
    day_game = {}
    game = []
    max_day_on = 0
    max_day_down = 0
    now_day = 0
    for i in list:
        play_time = i.play_time
        day = datetime.datetime.strptime(str(play_time.year) + '-' + str(play_time.month) + '-' + str(play_time.day),
                                         "%Y-%m-%d")
        if old_day != day:
            array.append(day)
            old_day = day
            game = []
        game.append(i.__getattribute__(label))
        day_game.update({str(day): game})

    last_day = 0
    for k, v in day_game.items():
        now_day = sum(v)
        if sum(v) > 0:
            flag = 1
        elif sum(v) == 0:
            flag = 0
        else:
            flag = -1
        if last_day == flag or flag == 0:
            tmp = tmp + flag
        else:
            last_day = flag
            tmp = 0
        if max_day_on < tmp:
            max_day_on = tmp
            print(tmp)
            print(k)
        if max_day_down > tmp:
            max_day_down = tmp
            # print(tmp)
            # print(k)
        # print(tmp)
        # print(k)
    two_day = sum(day_game.get(str(array[-1]))) + sum(day_game.get(str(array[-2])))
    three_day = sum(day_game.get(str(array[-1]))) + sum(day_game.get(str(array[-2]))) + sum(
        day_game.get(str(array[-3])))
    return max_day_on, max_day_down, tmp, now_day, two_day, three_day


