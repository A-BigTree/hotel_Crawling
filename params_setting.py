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
"""省、直辖市、自治区、特别行政区"""

URL_BOOKING = "https://www.booking.cn/searchresults.zh-cn.html"
"""使用的URL"""

PARAMS_URL = {
    "aid": 397645,
    "ss": None,     # 地区名称
    "lang": "zh-cn",
    "sb": 1,
    "src_elem": "sb",
    "src": "index",
    "group_adults": 2,
    "no_rooms": 1,
    "group_children": 0,
    "sb_travel_purpose": "leisure",
    "offset": 0      # 控制翻页
}
"""URL参数"""

PARAMS_REQUEST = {
    "User-Agent": None,
    "Cookie": None
}
