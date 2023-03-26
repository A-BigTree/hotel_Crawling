**@author: Shuxin_Wang**

**@time: 2023.03.24**

-----

软工课程项目需要*Booking*酒店数据，需要酒店的信息和图片，最后一共获得`2G+`的的数据，信息包括`10000+`酒店的基本数据，和`80000+`的酒店图片，因为数据量较大（~~我怕吃牢饭~~），这里并没有放出来，感兴趣或者有需求的bro~可以照着代码自己爬取一下（**友情提示：数据量较大，一时半会爬不完**）。

**<u>示例网址：</u>**

基于`地域名称`查询

- [搜索上海酒店_上海酒店查询_ Booking.com 缤客](https://www.booking.cn/searchresults.zh-cn.html?aid=397645&ss=上海&lang=zh-cn&sb=1&src_elem=sb&src=index&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset=0)

基于`dest_id`查询

- [搜索酒店_酒店查询_Booking.com缤客](https://www.booking.cn/searchresults.zh-cn.html?aid=397645&lang=zh-cn&sb=1&src_elem=sb&src=searchresults&dest_id=678&dest_type=region&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset=25)

----

# 1 路径说明

**|--config（配置文件夹）**

**|----|--backup（手动备份文件夹）**

**|----|--cookie.txt（cookie设置）**

**|----|--page_num.csv（城市相关信息记录）**

**|----|--user-agent.txt（用户客户端设置）**

**|--params_setting.py（相关参数设置）**

**|--crawling_process.py（爬取过程函数与主函数）**

|--data（爬取数据存放）

|----|--backup（手动备份文件夹）

|----|--image（酒店封面图）

|----|----|--0.jpg

|----|----|--...

|----|--info（酒店详细信息）

|----|----|--image（酒店详细照片）

|----|----|\----|--0（标号0-999的酒店照片）

|\----|\----|\----|\----|--0_0.jpg

|\----|\----|\----|\----|--0_1.jpg

|\----|\----|\----|\----|--...

|\----|\----|\----|--1000（标号1000-1999的照片）

|\----|\----|\----|\----|--1000_0.jpg

|\----|\----|\----|\----|--...

|\----|\----|\----|--...

|\----|\----|\----|--10000（标号大于10000的酒店照片）

|\----|\----|\----|\----|--10000_0.jpg

|\----|\----|\----|\----|--...

|\----|\----|--desc.csv（酒店的详细描述）

|\----|\----|--image.csv（酒店图片URL链接）

|\----|\----|--image_error.csv（图片爬取失败日志）

|\----|\----|--info.csv（酒店详细信息记录）

|\----|--hotels.csv（酒店具体页面链接记录）

|\----|--image_error.csv（封面图爬取失败日志）

----



- **<u>data数据文件夹没有放出来，需要自己新建不然会报错</u>**



# 2 配置文件

## 请求头配置

文件`cookie.txt`和`user-agent.txt`,可以通过在浏览器访问上面的示例网址，打开检查的网络模块可以看到具体的Cookie和User-Agent设置，直接把对应的值复制过去即可，同时如果需要其他添加其他参数，可以在`params_setting.py`中的`PARAMS_REQUEST`修改：

```python
PARAMS_REQUEST = {
    "User-Agent": None,
    "Cookie": None，
    # add params here
}
"""Parameters of request for *Booking*"""
```

同时在`config`文件夹里添加**<u>对应名称</u>**的`txt`文件，在初始化的时候自动读取：

```python
def init_params_request():
    """Init parameters using in request"""
    for key in PARAMS_REQUEST.keys():
        try:
            with open("config/" + key.lower() + ".txt", encoding='utf-8') as f:
                PARAMS_REQUEST[key] = f.readline().encode('utf-8').decode('latin1')
        except Exception as e:
            print(e)
            raise RuntimeError("Init process error.")
```

## 城市信息配置

城市配置的相关信息在 `config/page_num.csv`文件中，该csv文件的表头信息如下：

| 城市名称 | 所含酒店网页数 | Booking设置的目的地ID标识 |
| -------- | -------------- | ------------------------- |

要问我ID标识怎么得到的（~~我才不说是一个省份一个省份试出来的呢~~），咳咳所以不知道有没有时效性，大家且用且珍惜。

在整个程序运行开始之前，城市信息会自动初始化到`params_setting.py`中的`CON_INFO`中：

```python
CITY_INFO = {
    "city_num": 0,
    "city_list": []
}
"""The dict of cities' information"""


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
```

# 3 网址设置

## 请求基址

网址的请求基址为`params_setting.py`中的`URL_BOOKING`：

```python
URL_BOOKING = "https://www.booking.cn/searchresults.zh-cn.html"
"""URL using in query"""
```

所有的查询界面都是在此基址上进行请求参数的设置变化

## 基于城市名称的参数设置（不稳定不推荐）

```python
PARAMS_URL_CITY_NAME = {
    "aid": 3976,  # 访客ID(maybe)，具体情况需要更新
    "ss": None,  # 城市名称
    "lang": "zh-cn",  # Language
    "sb": 1,
    "src_elem": "sb",
    "src": "index",
    "group_adults": 2, # 要住两个成人
    "no_rooms": 1, # 需要几间房间
    "group_children": 0, # 居住孩子的数量
    "sb_travel_purpose": "leisure", # 订酒店的目的
    "offset": 0  # Page # 页面位移（一页一般为25个结果->（页面数-1）*25）
}
"""Parameters using city name in query URL"""
```

**<u>因为有点城市名称直接查询结果比较奇葩，不稳定，所以不推荐使用这种方法</u>**

## 基于城市ID的参数设置（推荐）

具体参数含义与上面的类似，具体城市的`dest_id`在城市信息字典中`CITY_INFO`中

```python
PARAMS_URL_CITY_ID = {
    "aid": 3976,
    "lang": "zh-cn",
    "sb": 1,
    "src_elem": "sb",
    "src": "searchresults",
    "dest_id": None,   # 城市ID
    "dest_type": "region",
    "group_adults": 2,
    "no_rooms": 1,
    "group_children": 0,
    "sb_travel_purpose": "leisure",
    "offset": 0  # Page
}
"""Parameters using city ID in query URL"""
```



# 4 解析路径

习惯使用`XPath`对网页进行解析，通用的请求解析函数如下：

```python
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
```

## 查询界面相关信息解析

```python
# 城市酒店查询结果页数
XPATH_HOTEL_PAGE_NUM = "//*[@id='search_results_table']/div[2]/div/div/div[4]/div[2]/nav/div/div[2]/ol//li/button/text()"
"""The number of hotels' page"""

# 城市查询结果汇总
XPATH_HOTEL_PAGE_TITLE = "//*[@id='right']/div[1]/div/div/div/h1/text()"
"""The title in this page"""

# 该页结果酒店名称列表
XPATH_HOTEL_PAGE_NAME = "//*[@id='search_results_table']/div[2]/div/div/div[3]//div/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()"
"""The name of hotel in the page"""

# 该页酒店详细信息链接列表
XPATH_HOTEL_PAGE_HREF = "//*[@id='search_results_table']/div[2]/div/div/div[3]//div/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a/@href"
"""The link of hotel in the link"""

# 该页酒店封面图片链接列表
XPATH_HOTEL_PAGE_IMAGE = "//*[@id='search_results_table']/div[2]/div/div/div[3]//div/div[1]/div[1]/div/a/img/@src"
"""The image of hotel in the page"""
```

## 酒店详情页面解析

```python
# 酒店星级
XPATH_HOTEL_STAR = "//*[@id='hp_hotel_name']/span/span[2]/div/span/div/span//span"
"""The star of hotel"""

# 酒店所在城市
XPATH_HOTEL_CITY = "//*[@id='breadcrumb']/ol//li/div/a/text()"
"""The city of the hotel"""

# 酒店名称
XPATH_HOTEL_NAME = "//*[@id='hp_hotel_name']/div/h2/text()"
"""The name of hotel"""

# 酒店详细地址
XPATH_HOTEL_ADDRESS = "//*[@id='showMap2']/span/text()"
"""The address of the hotel"""

# 酒店评分
XPATH_HOTEL_POINT = "//*[@id='js--hp-gallery-scorecard']/a/div/div/div/div[1]/text()"
"""The point of the hotel"""

# 酒店图片链接列表
XPATH_HOTEL_IMAGES = "//*[@id='hotel_main_content']//a/img/@src"
"""The images of the hotel"""

# 酒店详细描述
XPATH_HOTEL_DESC = "//*[@id='property_description_content']//p/text()"
"""The description of the hotel"""
```



# 5 运行过程

## 文字信息获取

1. 获取查询页面所有酒店的详细页面链接和封面图片链接并标号存放到`data/hotels.csv`文件：

- `get_all_city_hotel()`

`data/hotels.csv`表头含义：

| 名称 | 详细页面链接 | 省份 | offset | 封面图片链接 | 标号 |
| ---- | ------------ | ---- | ------ | ------------ | ---- |

2. 爬取所有酒店的详细页面，获取基本信息，详细描述存放到`data/info/desc.csv`中，图片链接放到`data/info/images.csv`中，其余信息放到`data/info/info.csv`中（所需时间很长很长，需要等待）：

- `get_all_hotel_info()`：出现报错可以调整开始位置`INDEX_START`继续进行爬取；

`data/info/desc.csv`表头含义：

| 标号 | 详细介绍 |
| ---- | -------- |

`data/info/images.csv`表头含义：

| 标号 | 图片链接 |
| ---- | -------- |

`data/info/info.csv`表头含义：

| 标号 | 名称 | 省份 | 地区 | 详细地址 | 评分 | 图片数量 | 星级 |
| ---- | ---- | ---- | ---- | -------- | ---- | -------- | ---- |

## 图片获取

图片获取通用函数如下：

```python
ef get_image_from_url(image_url: str, file_name: str):
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
```

1. 获取封面图片，将图片存放到`data/image/`文件夹中：

- `get_page_image()`

2. 获取酒店的所有图片，因数目较多（`7w+`）使用**<u>多线程技术</u>**，每1000家酒店为一组放在一个文件夹里：

- `get_all_images()`：可在该函数中修改线程数量和批次（需调整图片存放文件夹）

