# -*- coding:utf-8 -*-
# @author  : Shuxin_Wang
# @email   : shuxinwang662@gmail.com
# @time    : 2023/3/23 
# @function: parameters using for crawling
# @version : V1.0 
#

CITY_NAME = ['北京地区', '广东', '山东', '江苏', '河南', '上海地区', '河北', '浙江', '中国香港', '陕西', '湖南', '重庆地区',
             '福建', '天津地区', '云南', '四川', '广西', '安徽', '海南', '江西', '湖北', '山西', '辽宁', '黑龙江', '内蒙古',
             '澳门', '贵州', '甘肃', '青海', '新疆', '中国，西藏', '吉林', '宁夏']
"""Cities' name using in querying"""

CITY_NAME_DEST_ID_DICT = {
    "北京地区": 1221,
    "陕西": 685,
    "山东": 686,
    "天津地区": 684,
    "江苏": 683,
    "湖北": 682,
    "河南": 681,
    "海南": 680,
    "广西": 679,
    "广东": 678,
    "福建": 677,
    "重庆地区": 676,
    "安徽": 675,
    "上海": 3245,
    "河北": 3698,
    "浙江": 3243,
    "云南": 3244,
    "山西": 3246,
    "吉林": 3242,
    "中国香港": 95,
    "湖南": 3699,
    "四川": 3705,
    "江西": 3700,
    "辽宁": 3701,
    "内蒙古": 3702,
    "宁夏": 3703,
    "青海": 3704,
    "新疆": 3706,
    "中国，西藏": 3707,
    "甘肃": 3697,
    "黑龙江": 3696,
    "中国澳门": 124,
    "贵州": 4915,
}
"""Mapping for city name to destID in Booking"""

URL_BOOKING = "https://www.booking.cn/searchresults.zh-cn.html"
"""URL using in query"""

# -------------Parameters Setting

PARAMS_URL_CITY_NAME = {
    "aid": 397645,  # update
    "ss": None,  # City name
    "lang": "zh-cn",  # Language
    "sb": 1,
    "src_elem": "sb",
    "src": "index",
    "group_adults": 2,
    "no_rooms": 1,
    "group_children": 0,
    "sb_travel_purpose": "leisure",
    "offset": 0  # Page
}
"""Parameters using city name in query URL"""

PARAMS_URL_CITY_ID = {
    "aid": 397645,
    "lang": "zh-cn",
    "sb": 1,
    "src_elem": "sb",
    "src": "searchresults",
    "dest_id": None,
    "dest_type": "region",
    "group_adults": 2,
    "no_rooms": 1,
    "group_children": 0,
    "sb_travel_purpose": "leisure",
    "offset": 0  # Page
}
"""Parameters using city ID in query URL"""

PARAMS_REQUEST = {
    "User-Agent": None,
    "Cookie": None
}
"""Parameters of request for *Booking*"""

# ---------------XPath

XPATH_HOTEL_PAGE_NUM = "//*[@id='search_results_table']/div[2]/div/div/div[4]/div[2]/nav/div/div[" \
                       "2]/ol//li/button/text()"
"""The number of hotels' page"""

XPATH_HOTEL_NAME = "/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]//div/div[" \
                   "1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()"
"""The name of `No.%d` hotel"""

XPATH_HOTEL_POINT = "/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]//div/div[" \
                    "1]/div[2]/div/div/div/div[2]/div/div[1]/div/a/span/div/div[1]/text()"

XPATH_HOTEL_HREF = "/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]//div/div[" \
                   "1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a/@href"
"""The link of `No.%d` hotel page"""

XPATH_HOTEL_CITY = "/html/body/div[2]/div/div[1]/div/nav/ol//li/div/a/text()"
"""The city of the hotel"""

XPATH_HOTEL_ADDRESS = "/html/body/div[2]/div/div[6]/div[1]/div[1]/div[1]/div/div[2]/div[9]/p/span[1]/text()"
"""The address of the hotel"""

XPATH_HOTEL_IMAGES = "/html/body/div[2]/div/div[6]/div[1]/div[1]/div[1]/div/div[2]/div[11]/div/div/div[1]/div[" \
                     "6]/div/div//a/img/@src"
"""The images of the hotel"""

XPATH_HOTEL_DESC = "/html/body/div[2]/div/div[6]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div[3]/p[" \
                   "2]/text()"
"""The description of the hotel"""

XPATH_HOTEL_ROOM = "/html/body/div[2]/div/div[6]/div[1]/div[1]/div[3]/div/div[5]/div[3]/div[7]/section//div/div[" \
                   "1]/div[1]/a/span/text()"
"""The names of configure rooms"""

XPATH_HOTEL_CAPACITY = "/html/body/div[2]/div/div[6]/div[1]/div[1]/div[3]/div/div[5]/div[3]/div[7]/section//div/div[" \
                       "2]/div/div/@aria-label"
"""The capacity of rooms"""


# --------------------Init Processing


def init_params_request():
    """Init parameters using in request"""
    for key in PARAMS_REQUEST.keys():
        try:
            with open("data/" + key.lower() + ".txt", encoding='utf-8') as f:
                PARAMS_REQUEST[key] = f.readline().encode('utf-8').decode('latin1')
        except Exception as e:
            print(e)
            raise RuntimeError("Init process error.")
