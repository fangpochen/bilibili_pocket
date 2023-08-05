import copy
from datetime import datetime

import requests

from app import db
from app.models import Team, Data
from app.util import get_data

baseUrl = 'http://nba.win007.com/jsData/matchResult/'
qw = {'1': 4, '3': 2, '2': 10}
teams = db.session.query(Team).all()
plays = copy.deepcopy(teams)
db.session.close()


def insert_list(list, table):
    fourth_time = datetime.utcnow()
    array = []
    for i in list:
        obj = {}
        if i == None:
            continue
        for key in i.__mapper__.c.keys():
            value = getattr(i, key)
            obj.update({key: value})
        array.append(obj)
    try:
        db.session.execute(
            table.__table__.insert(),
            array
        )
        db.session.commit()
    except Exception as e:
        print(e.args)
    five_time = datetime.utcnow()
    print((five_time - fourth_time).total_seconds())


def save_list(list):
    first_time = datetime.utcnow()
    for i in list:
        try:
            db.session.add(i)
            db.session.commit()
        except Exception as e:
            print(e.args)
            db.session.rollback()
            continue
    second_time = datetime.utcnow()
    print((second_time - first_time).total_seconds())


def data():
    array = [3, 4, 5, 6, 7, 8, 9, 10]
    season = '20-21'
    num = '2'
    month = '_2021_5'
    month = ''
    version = 'l1_{}{}'.format(num, month)
    label = season + '/' + version
    teams = db.session.query(Team).all()
    url = 'http://nba.win007.com/jsData/matchResult/{}.js?version=2021101022'.format(label)
    text = requests.get(url).text
    array = text.replace('\n', '').split(";")
    data = array[qw.get(num)]
    data = data[data.find('='):len(data)].replace('\'', '').split(']')
    result = get_data(data, teams)
    insert_list(result, Data)


def GetPreseasonData():
    for i in range(10, 22):
        startYear = str(i)
        endYear = str(i + 1)
        if len(startYear) == 1:
            startYear = '0' + startYear
        if len(endYear) == 1:
            endYear = '0' + endYear
        matchYear = startYear + '-' + endYear
        url = baseUrl + '{}/l1_3.js?version=2021101022'.format(matchYear)
        text = requests.get(url).text
        array = text.replace('\n', '').split(";")
        data = array[qw.get('3')]
        data = data[data.find('='):len(data)].replace('\'', '').split(']')
        result = get_data(data, plays)
        insert_list(result, Data)
        # save_list(result)


def GetRegularSeasonData():
    for i in range(10, 22):
        startYear = str(i)
        endYear = str(i + 1)
        if len(startYear) == 1:
            startYear = '0' + startYear
        if len(endYear) == 1:
            endYear = '0' + endYear
        matchYear = startYear + '-' + endYear
        for j in range(1, 7):  # 常规赛后半程
            secondYear = '20' + endYear
            url = baseUrl + '{}/l1_1_{}_{}.js?version=2021101022'.format(matchYear, secondYear, str(j))
            resp = requests.get(url, verify=False)
            if '!DOCTYPE html PUBLIC' in resp.text:
                continue
            else:
                text = resp.text
                array = text.replace('\n', '').split(";")
                data = array[qw.get('1')]
                data = data[data.find('='):len(data)].replace('\'', '').split(']')
                result = get_data(data, plays)
                # insert_list(result, Data)
                save_list(result)

        for j in range(7, 13):  # 常规赛前半程
            firstYear = '20' + startYear
            url = baseUrl + '{}/l1_1_{}_{}.js?version=2021101022'.format(matchYear, firstYear, str(j))
            resp = requests.get(url, verify=False)
            if '!DOCTYPE html PUBLIC' in resp.text:
                continue
            else:
                text = resp.text
                array = text.replace('\n', '').split(";")
                data = array[qw.get('1')]
                data = data[data.find('='):len(data)].replace('\'', '').split(']')
                result = get_data(data, plays)
                # insert_list(result, Data)
                save_list(result)


def GetPostseasonData():
    for i in range(4, 22):
        startYear = str(i)
        endYear = str(i + 1)
        if len(startYear) == 1:
            startYear = '0' + startYear
        if len(endYear) == 1:
            endYear = '0' + endYear
        matchYear = startYear + '-' + endYear
        url = baseUrl + '{}/l1_2.js?version=2021101022'.format(matchYear)
        resp = requests.get(url, verify=False)
        with open('./origindata/PostseasonData{}.txt'.format(matchYear), 'w') as f:
            f.write(resp.text)




if __name__ == '__main__':
    # get_dish_data()
    # get_home_data()
    # get_size_data()
    GetPreseasonData()
    # GetRegularSeasonData()
