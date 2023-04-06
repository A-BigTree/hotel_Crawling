# -*- coding:utf-8 -*-
# @author  : Shuxin_Wang
# @email   : shuxinwang662@gmail.com
# @time    : 2023/3/24 
# @function: the functions using for crawling process
# @version : V1.0 
#
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union, List
import requests
from lxml import etree
from requests import Response
from params_setting import *
from queue import Queue

# ----------Init processing
init_processing()


# ----------Request and analysis
def get_response(url: str, params: dict = None, headers: dict = PARAMS_REQUEST) -> Response:
    """Get `Response` Object using URL and Request parameters"""
    try:
        response = requests.get(url=url,
                                params=params,
                                headers=headers)
    except Exception as e:
        print(e)
        raise RuntimeError("Request error.")
    return response


def xpath_analysis(response: Response, xpath_: Union[str, List[str]]) -> dict:
    """Analysis article from response using list of xpath"""
    response.encoding = "utf-8"
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
                                 xpath_=[XPATH_HOTEL_PAGE_NAME,
                                         XPATH_HOTEL_PAGE_HREF,
                                         XPATH_HOTEL_PAGE_IMAGE])
        hotel_names = results[XPATH_HOTEL_PAGE_NAME]
        hotel_hrefs = results[XPATH_HOTEL_PAGE_HREF]
        hotel_image = results[XPATH_HOTEL_PAGE_IMAGE]
        print(f"Page hotel num: {len(hotel_names)}")
        csv_list = list()
        for j in range(len(hotel_names)):
            csv_list.append([hotel_names[j], hotel_hrefs[j], city_name, offset, hotel_image[j]])
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
    data_list = read_csv("data/hotels_v2.csv")
    for i in range(len(data_list)):
        data_list[i].append(i)
    write_csv("data/hotels.csv", data_list)


def get_hotel_info(url_hotel: str) -> dict:
    """Get a hotel information to dict data"""
    response = get_response(url_hotel)
    print(response.url)
    results = xpath_analysis(response=response,
                             xpath_=[XPATH_HOTEL_CITY,
                                     XPATH_HOTEL_NAME,
                                     XPATH_HOTEL_ADDRESS,
                                     XPATH_HOTEL_POINT,
                                     XPATH_HOTEL_IMAGES,
                                     XPATH_HOTEL_DESC,
                                     XPATH_HOTEL_STAR])
    city = results[XPATH_HOTEL_CITY]
    name = results[XPATH_HOTEL_NAME]
    address = results[XPATH_HOTEL_ADDRESS]
    point = results[XPATH_HOTEL_POINT]
    images = results[XPATH_HOTEL_IMAGES]
    desc = results[XPATH_HOTEL_DESC]
    star = len(results[XPATH_HOTEL_STAR])
    result_dict = {
        "name": name[0].strip("\n"),
        "star": star,
        "city": {
            "mun": "",
            "pro": ""
        },
        "addr": "null",
        "point": "null",
        "images": images,
        "desc": ""
    }
    for i in range(len(city)):
        city[i] = city[i].strip('\n')
    result_dict["city"]["pro"] = city[2]
    result_dict["city"]["mun"] = "，".join(city[3::])
    if len(address) > 0:
        result_dict['addr'] = address[0].strip('\n')
    if len(point) > 0:
        result_dict['point'] = point[0]
    result_dict['desc'] = "\n".join(desc)
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
        try:
            for data_ in read_data:
                href = data_[1]
                index_ = data_[-1]
                result_dict = get_hotel_info(href)
                print(f"Index: {index_}, Hotel: {result_dict['name']}, Star: {result_dict['star']}")
                print(f"City: ({result_dict['city']['pro']}, [{result_dict['city']['mun']}])")
                write_csv("data/info/info.csv",
                          [[index_, result_dict['name'], result_dict['city']['pro'], result_dict['city']['mun'],
                            result_dict['addr'], result_dict['point'], len(result_dict['images']),
                            result_dict['star']]])
                print(f"Desc length: char({len(result_dict['desc'])})")
                write_csv("data/info/desc.csv",
                          [[index_, result_dict['desc']]])
                print(f"Images number: {len(result_dict['images'])}")
                image_li = list()
                for image in result_dict['images']:
                    image_li.append([index_, image])
                if len(image_li) > 0:
                    write_csv("data/info/image.csv", image_li)
                print()
        except Exception as e:
            print(e)
            start = int(index_)
            time.sleep(120)
        time.sleep(10)


def get_image_from_url(image_url: str, file_name: str):
    """Get image from a image url"""
    try:
        response = get_response(image_url)
    except Exception as e:
        print(e)
        raise RuntimeError("Get image error")
    if response.status_code != 200:
        raise RuntimeError
    try:
        with open(file_name + ".jpg", "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(e)
        raise RuntimeError("Write image error")


def get_page_image():
    """Get hotels images from query page"""
    start = 0
    exp = re.compile(r"/square.+/")
    while True:
        read_data = read_csv("data/hotels.csv", batch=(start, start + BATCH_SETTING))
        start += BATCH_SETTING
        if len(read_data) == 0:
            break
        print(f"Loading images: {len(read_data)}")
        err = 0
        for data in read_data:
            index = data[-1]
            url_read = data[-2]
            url_image = re.sub(exp, "/square500/", url_read)
            try:
                get_image_from_url(url_image, "data/image/" + index)
            except RuntimeError:
                write_csv("data/image_error.csv", [[index, url_image]])
                err += 1
        print(f"Success: {len(read_data) - err}, Error: {err}")
        print()
        time.sleep(10)


class HotelImage:
    """The class to record for crawling images info"""

    def __init__(self, index_: str, id_: str, url_: str):
        self.index_ = index_
        self.id_ = id_
        self.url_ = url_


class ImageCrawling:
    """The class to manage crawling images using multithread"""

    def __init__(self, batch: Tuple[int, int], m_num: int = 10):
        self.batch = batch
        self.m_num = m_num
        self.queue = Queue()

    def set_batch(self, batch: Tuple[int, int]):
        self.batch = batch

    def set_num(self, m_num: int):
        self.m_num = m_num

    def init_queue(self):
        while not self.queue.empty():
            self.queue.get()
        data_list = read_csv("data/info/image.csv")
        for data in data_list:
            if self.batch[0] <= int(data[0]) < self.batch[1]:
                image_url = re.sub(r"/max.+/", "/max600/", data[1])
                image_url = re.sub(r"/square.+/", "/square600/", image_url)
                self.queue.put(HotelImage(data[0], data[2], image_url))

    def __function__(self, cache_: Queue):
        while not self.queue.empty():
            entities: HotelImage = self.queue.get()
            try:
                get_image_from_url(entities.url_,
                                   "data/info/image/" + str(self.batch[0]) + "/" + entities.index_ + "_" + entities.id_)
            except RuntimeError:
                cache_.put(entities)
        self.queue.task_done()

    def run(self):
        self.init_queue()
        cache_ = Queue()
        start = time.time()
        print(f"Batch: {self.batch}")
        while True:
            print(f"Images num: {self.queue.qsize()}, Threads: {self.m_num}")
            with ThreadPoolExecutor(max_workers=self.m_num) as pool:
                for i in range(self.m_num):
                    pool.submit(self.__function__, cache_)
            print(f"Error Images: {cache_.qsize()}")
            while not cache_.empty():
                entity: HotelImage = cache_.get()
                self.queue.put(entity)
                write_csv("data/info/image_error.csv", [[entity.index_, entity.id_, entity.url_]])
            if self.queue.empty():
                break
            else:
                print("Wait 30s to re-get error images")
            time.sleep(30)
        end = time.time()
        print(f"Cost time: {end - start}s\n")
        time.sleep(60)


def get_all_images():
    """Get all hotel images"""
    crawling_process = ImageCrawling(batch=(0, 0), m_num=10)
    for i in range(11):
        crawling_process.set_batch((i * 1000, (i + 1) * 1000))
        crawling_process.run()
