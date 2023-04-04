# -*- coding:utf-8 -*-
# @author  : Shuxin_Wang
# @email   : shuxinwang662@gmail.com
# @time    : 2023/4/3 
# @function: some functions for pretreatment process
# @version : V1.0 
#
import re
from crawling_process import *

XPATH_PROVINCE = "//td/a/text()"

XPATH_PROVINCE_HREF = "//td/a/@href"

'''
response = get_response(url="http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/index.html")
print(response.status_code)
result = xpath_analysis(response, [XPATH_PROVINCE, XPATH_PROVINCE_HREF])

result_data = list()
for i in range(len(result[XPATH_PROVINCE])):
    result_data.append([result[XPATH_PROVINCE][i], result[XPATH_PROVINCE_HREF][i]])
write_csv("data/province.csv", result_data)'''

URL_ = "http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/"
XPATH_CITY = "//tr/td[2]/a/text()"
XPATH_CITY_HREF = "//tr/td[2]/a/@href"
XPATH_CITY_CODE = "//tr/td[1]/a/text()"

'''
read_data = read_csv("data/province.csv")
for data in read_data:
    response = get_response(URL_ + data[1])
    results = xpath_analysis(response, [XPATH_CITY, XPATH_CITY_HREF, XPATH_CITY_CODE])
    city = results[XPATH_CITY]
    city_href = results[XPATH_CITY_HREF]
    city_code = results[XPATH_CITY_CODE]
    results_data = list()
    for i in range(len(city)):
        if city[i] == "市辖区":
            city[i] = data[0]
        results_data.append([data[0], city[i], city_href[i], city_code[i]])
    print(results_data)
    write_csv("data/city.csv", results_data)
    time.sleep(2)'''

'''
read_data = read_csv("data/city.csv")
for data in read_data:
    response = get_response(URL_ + data[2])
    results = xpath_analysis(response, [XPATH_CITY, XPATH_CITY_HREF, XPATH_CITY_CODE])
    city = results[XPATH_CITY]
    city_href = results[XPATH_CITY_HREF]
    city_code = results[XPATH_CITY_CODE]
    results_data = list()
    for i in range(len(city)):
        results_data.append([data[0], data[1], city[i], city_href[i], city_code[i]])
    print(results_data)
    write_csv("data/county.csv", results_data)
    time.sleep(0.5)'''

REG_EXP = ['经济开发区', '经济技术开发区', '高新技术产业开发区',
           '左旗', '右旗', '矿区', '联合旗', '自治旗', '自治县', "壮族自治区", "自治州",
           "回族自治区", "维吾尔自治区", "自治区", '县', '区', '新区', '市', '旗', "省", ]

'''
city_data = read_csv("data/county.csv")
result_data = list()
for city in city_data:
    pro = city[0]
    ci = city[1]
    county = city[2]
    for reg in REG_EXP:
        if len(pro) == len(city[0]) and len(city[0]) > 2:
            pro = city[0].replace(reg, "")
        if len(ci) == len(city[1]) and len(city[1]) > 2:
            ci = city[1].replace(reg, "")
        if len(county) == len(city[2]) and len(city[2]) > 2:
            county = city[2].replace(reg, "")
    result_data.append([city[0], city[1], city[2], pro, ci, county])
write_csv("data/pre_city.csv", result_data)'''

'''
hotels_data = read_csv("data/info/info.csv")
hotels_desc = read_csv("data/info/desc.csv")
city_data = read_csv("data/pre_city.csv")
num = 0
result_data = list()
for i in range(len(hotels_data)):
    hotel = hotels_data[i]
    desc = hotels_desc[i]
    flag = False
    for city in city_data:
        if (city[2] in hotel[4] or city[2] in desc[1]) and (city[3] in hotel[2] or city[3] in hotel[3]):
            flag = True
            result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
            break
    if not flag:
        for city in city_data:
            if (city[5] in hotel[4] or city[5] in hotel[3] or city[5] in desc[1]) and (city[3] in hotel[2] 
                                                                                       or city[3] in hotel[3]):
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        for city in city_data:
            if city[5] in hotel[1] and (city[3] in hotel[2] or city[3] in hotel[3]):
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        for city in city_data:
            if (city[4] in hotel[4] or city[4] in hotel[3] or city[4] in desc[1]) and (city[3] in hotel[2] 
                or city[3] in hotel[3]):
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        for city in city_data:
            if city[4] in hotel[1] and (city[3] in hotel[2] or city[3] in hotel[3]):
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break

    if not flag:
        for city in city_data:
            if city[2] in hotel[4]:
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        for city in city_data:
            if city[5] in hotel[4] or city[5] in hotel[3]:
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        for city in city_data:
            if city[5] in hotel[1]:
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        for city in city_data:
            if city[4] in hotel[4] or city[4] in hotel[3]:
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        for city in city_data:
            if city[4] in hotel[1]:
                flag = True
                result_data.append([hotel[0], city[0], city[1], city[2], hotel[4]])
                break
    if not flag:
        num += 1
        print(hotel[0:5], desc[1])
write_csv("data/info/address.csv", result_data)'''
