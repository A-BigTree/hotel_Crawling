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


if __name__ == "__main__":
    print(CITY_INFO)
