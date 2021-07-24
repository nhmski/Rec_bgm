# -*- coding: utf-8 -*-
"""
The code is supplied with user Oalvay, the original link to https://github.com/oalvay/projects/blob/master/web-crawler/bgm3.py
Thank you very much.
"""
from bs4 import BeautifulSoup
import requests, re, time


global base, filename, errorfile
base = 'http://mirror.bgm.rin.cat'
filename = "data/user_now.csv"
errorfile = "debug.txt"

type_ = "anime"

# 返回网页源代码
def get_html(url):
    request = requests.get(url)
    while 502 <= request.status_code <= 503:
        time.sleep(2)
        request = requests.get(url)
    request.encoding = "UTF-8"
    if request.status_code != 200:
        print("url:", url, ", code:", request.status_code, request.reason)
    return request.status_code, request.reason, BeautifulSoup(request.text, "html.parser")


def get_user(user):
    """ user: str, user id
        return a list of bs4 Tags"""
    _, _, html = get_html(base + f"/user/{user}")
    html = html.find("div", id=type_)
    if html is None:
        return []
    else:
        return html.findAll("a", href= \
            re.compile(f"/{type_}/list/.*/(wish|collect|on_hold|dropped|do)"))

# 获取相应的id,评分
def get_info(item, status):
    """ item: bs4 Tags, status: str
        return anime id, status, date to watch, rate, comment"""
    info_list = [
        item.get("id")[5:],  # anime id    # e.g.'item_323747'从5开始取后面的
        status,
        item.find("span", class_=re.compile("^starlight stars\d+$")),  # rate
        # span 在span元素中找，且class的类别一致  
    ]
    info_list[2] = info_list[2].get("class")[1][5:] if info_list[2] is not None else "0"
    return info_list

# 将评分数据写入file
def process_user(user):
    try: 
        for i in get_user(user):
            html, page = "start", 1
            while html:
                url = base + i.get("href")  # url+f"?page={page}"
                status = i.get("href").split("/")[-1]
                _, _, html = get_html(url + f"?page={page}") # 收集页面的源代码 有多页page
                # find,find_all的简单版，只找一个
                html = html.find('ul', id='browserItemList').findAll("li", re.compile("^item (odd|even) clearit$"))
                for item in html: # 具体到该页面有的每个条目
                    with open(filename, "a") as f:
                        f.write("\t".join([str(user)] + get_info(item, status)) + "\n")

                page += 1
    except AttributeError: 
        with open(errorfile, "a") as f:
            f.write(url + f"?page={page}" + "\n")
    except Exception as e:
        print(user, e)
        time.sleep(1200)
        process_user(user)



