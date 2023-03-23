# -*- coding:utf-8 -*-
# @author  : Shuxin_Wang
# @email   : shuxinwang662@gmail.com
# @time    : 2023/3/23 
# @function: parameters using for crawling
# @version : V1.0 
#

CITY_NAME = ['北京', '广东', '山东', '江苏', '河南', '上海', '河北', '浙江', '香港', '陕西', '湖南', '重庆', '福建',
             '天津', '云南', '四川', '广西', '安徽', '海南', '江西', '湖北', '山西', '辽宁', '台湾', '黑龙', '内蒙古',
             '澳门', '贵州', '甘肃', '青海', '新疆', '西藏', '吉林', '宁夏']
"""Cities' name using in querying"""

URL_BOOKING = "https://www.booking.cn/searchresults.zh-cn.html"
"""URL using in query"""

# -------------Parameters Setting

PARAMS_URL = {
    "aid": 397645,
    "ss": None,  # City name
    "lang": "zh-cn",  # Language
    "sb": 1,
    "src_elem": "sb",
    "src": "index",
    "group_adults": 2,
    "no_rooms": 1,
    "group_children": 0,
    "sb_travel_purpose": "leisure",
    "offset": 0   # Page
}
"""Parameters using in query URL"""

PARAMS_REQUEST = {
    "User-Agent": None,
    "Cookie": None
}
"""Parameters of request for *Booking*"""

# ---------------XPath

XPATH_HOTEL_NUM = "/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]/div"
"""The number of hotels in this page"""

XPATH_HOTEL_NAME = "/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]/div[%d]/div[" \
                   "1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()"
"""The name of `No.%d` hotel"""

XPATH_HOTEL_HREF = "/html/body/div[3]/div/div[5]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]/div[%d]/div[" \
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
                PARAMS_REQUEST[key] = f.readline()
        except Exception as e:
            print(e)
            raise RuntimeError("初始化错误.")
