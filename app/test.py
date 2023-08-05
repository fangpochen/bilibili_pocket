import json

import requests


def get_sms(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data


def get_bilibili_sms(phone_num, url):
    data = get_sms(url)
    for i in data:
        content = i['content']
        if phone_num[-4:] == i['simnum'][-4:]:
            if "验证码" in content:
                return content[9:15]
    return ''


if __name__ == '__main__':
    url = 'http://sms.newszfang.vip:3000/api/smslist?token=Jq5LduJnXhW5fvvZnQQez8'
    print(get_bilibili_sms("19209369398", url))
