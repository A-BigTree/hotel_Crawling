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
init_params_request()


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


def xpath_analysis(response: Response, xpath_: Union[str, List[str]]) -> list:
    """Analysis article from response using list of xpath"""
    xpath_data = etree.HTML(response.text)
    if isinstance(xpath_, str):
        xpath_ = [xpath_]
    results = list()
    for xp in xpath_:
        result = xpath_data.xpath(xp)
        results.append(result)
    return results


def get_city_page_num():
    """Print cities' page number"""
    nums = list()
    for city in CITY_NAME:
        PARAMS_URL['ss'] = city.encode('utf-8')
        response = get_response(url=URL_BOOKING,
                                params=PARAMS_URL)
        print(response.url)
        results = xpath_analysis(response, XPATH_HOTEL_PAGE_NUM)
        print(results)
        num: str = results[0][-1]
        nums.append(int(num))
        time.sleep(3)
    print("CITY_HOTEL_NUM =", nums)


if __name__ == "__main__":
    get_city_page_num()
