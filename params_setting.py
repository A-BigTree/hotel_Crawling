# -*- coding:utf-8 -*-
# @author  : Shuxin_Wang
# @email   : shuxinwang662@gmail.com
# @time    : 2023/3/23 
# @function: parameters using for crawling
# @version : V1.0 
#
import csv

from typing import Tuple

CITY_INFO = {
    "city_num": 0,
    "city_list": []
}
"""The dict of cities' information"""

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

XPATH_HOTEL_PAGE_TITLE = "//*[@id='right']/div[1]/div/div/div/h1/text()"
"""The title in this page"""

XPATH_HOTEL_PAGE_NAME = "//*[@id='search_results_table']/div[2]/div/div/div[3]//div/div[1]/div[2]/div/div/div/div[" \
                   "1]/div/div[1]/div/h3/a/div[1]/text()"
"""The name of hotel in the page"""

XPATH_HOTEL_PAGE_HREF = "//*[@id='search_results_table']/div[2]/div/div/div[3]//div/div[1]/div[2]/div/div/div/div[" \
                   "1]/div/div[1]/div/h3/a/@href"
"""The link of hotel in the link"""

XPATH_HOTEL_PAGE_IMAGE = "//*[@id='search_results_table']/div[2]/div/div/div[3]//div/div[1]/div[1]/div/a/img/@src"
"""The image of hotel in the page"""

XPATH_HOTEL_STAR = "//*[@id='hp_hotel_name']/span/span[2]/div/span/div/span//span"
"""The star of hotel"""

XPATH_HOTEL_CITY = "//*[@id='breadcrumb']/ol//li/div/a/text()"
"""The city of the hotel"""

XPATH_HOTEL_NAME = "//*[@id='hp_hotel_name']/div/h2/text()"
"""The name of hotel"""

XPATH_HOTEL_ADDRESS = "//*[@id='showMap2']/span/text()"
"""The address of the hotel"""

XPATH_HOTEL_POINT = "//*[@id='js--hp-gallery-scorecard']/a/div/div/div/div[1]/text()"
"""The point of the hotel"""

XPATH_HOTEL_IMAGES = "//*[@id='hotel_main_content']//a/img/@src"
"""The images of the hotel"""

XPATH_HOTEL_DESC = "//*[@id='property_description_content']//p/text()"
"""The description of the hotel"""

XPATH_HOTEL_ROOM = "//*[@id='rooms_table']/div[3]/section//div/div[1]/div[1]/a/span/text()"
"""The names of configure rooms"""

XPATH_HOTEL_CAPACITY = "//*[@id='rooms_table']/div[3]/section//div/div[2]/div/div/@aria-label"
"""The capacity of rooms"""


def write_csv(file_name: str, data: list, encoding: str = 'utf-8'):
    """Write 2D data to csv file"""
    try:
        with open(file_name, 'a', encoding=encoding, newline='') as f:
            writer = csv.writer(f)
            for da in data:
                writer.writerow(da)
    except Exception as e:
        print(e)
        print(f"File:{file_name}, Write Failed")


def read_csv(file_name: str, batch: Tuple[int, int] = None, encoding: str = 'utf-8') -> list:
    """Read 2D data from csv file"""
    data_list = list()
    try:
        with open(file_name, 'r', encoding=encoding) as f:
            reader = csv.reader(f)
            if batch is None:
                for data in reader:
                    data_list.append(data)
            else:
                i = 0
                for data in reader:
                    if batch[0] <= i < batch[1]:
                        data_list.append(data)
                    i += 1
    except Exception as e:
        print(e)
    return data_list


# --------------------Init Processing


def init_params_request():
    """Init parameters using in request"""
    for key in PARAMS_REQUEST.keys():
        try:
            with open("config/" + key.lower() + ".txt", encoding='utf-8') as f:
                PARAMS_REQUEST[key] = f.readline().encode('utf-8').decode('latin1')
        except Exception as e:
            print(e)
            raise RuntimeError("Init process error.")


def init_city_dict():
    """Init city dict using .csv file"""
    city_list = read_csv(file_name="config/page_num.csv")
    CITY_INFO['city_num'] = len(city_list)
    for info in city_list:
        CITY_INFO['city_list'].append({
            "name": info[0],
            "page_num": info[1],
            "dest_id": info[2]
        })


def init_processing():
    """Init processing"""
    init_params_request()
    init_city_dict()
