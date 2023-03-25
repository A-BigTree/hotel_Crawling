# -*- coding:utf-8 -*-
# @author  : Shuxin_Wang
# @email   : shuxinwang662@gmail.com
# @time    : 2023/3/24 
# @function: the script is used to do something.
# @version : V1.0 
#
import time
from typing import Union, List
import requests
from lxml import etree
from requests import Response
from params_setting import *

# ----------Init processing
init_processing()


# ----------Request and analysis
def get_response(url: str, params: dict = None) -> Response:
    """Get `Response` Object using URL and Request parameters"""
    try:
        response = requests.get(url=url,
                                params=params,
                                headers=PARAMS_REQUEST)
    except Exception as e:
        print(e)
        raise RuntimeError("Request error.")
    return response


def xpath_analysis(response: Response, xpath_: Union[str, List[str]]) -> dict:
    """Analysis article from response using list of xpath"""
    xpath_data = etree.HTML(response.text)
    if isinstance(xpath_, str):
        xpath_ = [xpath_]
    results = dict()
    for xp in xpath_:
        result = xpath_data.xpath(xp)
        results[xp] = result
    return results


def get_city_hotel(city_info: dict):
    """Get hotels from a city"""
    offset = 0
    city_name = city_info['name']
    city_page = int(city_info['page_num'])
    dest_id = int(city_info['dest_id'])
    PARAMS_URL_CITY_ID['dest_id'] = dest_id
    for i in range(city_page):
        PARAMS_URL_CITY_ID['offset'] = offset
        print(f"city: {city_name}, offset: {offset}")
        response = get_response(url=URL_BOOKING,
                                params=PARAMS_URL_CITY_ID)
        results = xpath_analysis(response=response,
                                 xpath_=[XPATH_HOTEL_PAGE_NAME, XPATH_HOTEL_PAGE_HREF])
        hotel_names = results[XPATH_HOTEL_PAGE_NAME]
        hotel_hrefs = results[XPATH_HOTEL_PAGE_HREF]
        print(f"Page hotel num: {len(hotel_names)}")
        csv_list = list()
        for j in range(len(hotel_names)):
            csv_list.append([hotel_names[j], hotel_hrefs[j], city_name, offset])
        offset += len(hotel_names)
        write_csv(file_name="data/hotels.csv",
                  data=csv_list)
        print()
        time.sleep(3)
    time.sleep(10)


def get_all_city_hotel():
    """Get all hotel in all city"""
    for city_in in CITY_INFO['city_list']:
        get_city_hotel(city_in)


def get_hotel_info(url_hotel: str) -> dict:
    """Get a hotel information to dict data"""
    response = get_response(url_hotel)
    results = xpath_analysis(response=response,
                             xpath_=[XPATH_HOTEL_CITY,
                                     XPATH_HOTEL_NAME,
                                     XPATH_HOTEL_ADDRESS,
                                     XPATH_HOTEL_POINT,
                                     XPATH_HOTEL_IMAGES,
                                     XPATH_HOTEL_DESC])
    city = results[XPATH_HOTEL_CITY]
    name = results[XPATH_HOTEL_NAME]
    address = results[XPATH_HOTEL_ADDRESS]
    point = results[XPATH_HOTEL_POINT]
    images = results[XPATH_HOTEL_IMAGES]
    desc = results[XPATH_HOTEL_DESC]
    result_dict = {
        "name": name[0],
        "city": {
            "mun": city[-1].strip('\n'),
            "pro": city[-2].strip('\n')
        },
        "addr": "null",
        "point": "null",
        "images": images,
        "desc": ""
    }
    if len(address) > 0:
        result_dict['addr'] = address[0].strip('\n')
    if len(point) > 0:
        result_dict['point'] = point[0]
    for de in desc:
        result_dict['desc'] += (de + '\n')
    return result_dict


INDEX_START = 0
"""The index of start"""

BATCH_SETTING = 100
"""The query number per batch"""


def get_all_hotel_info():
    """Get all information start by `Index_START`"""
    start = INDEX_START
    index_ = INDEX_START
    while True:
        read_data = read_csv(file_name="data/hotels.csv",
                             batch=(start, start + BATCH_SETTING))
        start += BATCH_SETTING
        if len(read_data) == 0:
            break
        for data_ in read_data:
            href = data_[1]
            result_dict = get_hotel_info(href)
            print(f"Index: {index_}, Hotel: {result_dict['name']}")
            print(f"City: ({result_dict['city']['pro']}, {result_dict['city']['mun']})")
            write_csv("data/info/info.csv",
                      [[index_, result_dict['name'], result_dict['city']['pro'], result_dict['city']['mun'],
                        result_dict['addr'], result_dict['point'], len(result_dict['images']), href]])
            print(f"Desc length: char{len(result_dict['desc'])}")
            write_csv("data/info/desc.csv",
                      [[index_, result_dict['desc']]])
            print(f"Images number: {len(result_dict['images'])}")
            image_li = list()
            for image in result_dict['images']:
                image_li.append([index_, image])
            if len(image_li) > 0:
                write_csv("data/info/image.csv", image_li)
            index_ += 1
            print()
            time.sleep(1)


if __name__ == "__main__":
    # get_all_city_hotel()
    get_all_hotel_info()
