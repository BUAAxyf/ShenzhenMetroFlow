"""
目标元素为canvas标签,id随机。
XPath为/html/body/div[2]/div/div/div/div/canvas
收录于https://www.szmc.net/shentieyunying/yunyingfuwu/meiyuekeliu/index.html页面
dependencies: selenium, time, requests, lxml, os
"""
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import requests

from lxml import html


def get_url_list(url = "https://www.szmc.net/shentieyunying/yunyingfuwu/meiyuekeliu/index.html"):
    """
    获取index页面下所有要下载的url
    :param url:
    :return:
    """
    # 发送 GET 请求获取页面内容
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    # }
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # 解析网页内容
    tree = html.fromstring(response.content)

    # 定义目标 XPath 路径
    xpath_pattern = '/html/body/div[5]/div[2]/div[1]/a[{}]'

    # 存储链接的列表
    url_list = []

    # 遍历并获取从 a[1] 到 a[12] 的链接
    for i in range(1, 13):
        xpath = xpath_pattern.format(i)
        # 使用 XPath 提取链接
        link = tree.xpath(f'{xpath}/@href')
        if link:
            url_list.append("https://www.szmc.net" + link[0])  # 取出 href 属性的值

    return url_list


def get_canvas(url):
    """
    爬取url页面的canvas元素
    :param url:
    :return:
    """
    # 启动浏览器
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 2000)  # 足够大的浏览器窗口

    # 访问页面
    driver.get(url)

    # 等待页面加载
    for i in range(100):
        time.sleep(1)

        if driver.execute_script("return document.readyState") == "complete":
            break

    if driver.execute_script("return document.readyState") != "complete":
        print(f"Failed to load {url}.")
        return None

    time.sleep(5)

    # 获取canvas元素
    canvas = driver.find_element(By.ID, "canvasDiv").find_element(By.TAG_NAME, "canvas")

    # 获取title
    title = driver.find_element(By.XPATH, '/html/body/div[2]/div/h3').text

    # 转化为png
    canvas_data = canvas.screenshot_as_png

    driver.quit()

    return title, canvas_data


def get_title(url):
    # 发送 GET 请求获取页面内容
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    # 解析网页内容
    tree = html.fromstring(response.content)

    # 使用 XPath 提取指定位置的标题（h3 标签内容）
    title = tree.xpath('/html/body/div[2]/div/h3/text()')

    # 返回提取的标题内容，如果没有找到则返回 None
    if title:
        # print(f"Title found in {url}: {title[0]}")
        return title[0].strip()  # 获取文本并去除首尾空格
    else:
        print(f"Title not found in {url}.")
        return None


def save_pic(data, save_path = "web_data", file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())):

    with open(f"{save_path}/{file_name}.png", "wb") as f:
        f.write(data)


def save_title(title, save_path="title.txt"):

    # 检查
    if not os.path.exists(save_path):
        with open(save_path, "wb") as f:
            pass

    with open(save_path, "ab") as f:
        f.write(title.encode("utf-8"))
        f.write(b"\n")


def crawl_url_list(url_list, save_path ="web_data"):

    for url in url_list:
        for u in get_url_list(url):

            title, canvas_data = get_canvas(u)

            if canvas_data:
                print(f"Canvas data found in {u}.")

            else:
                print(f"Canvas data not found in {u}.")
                continue

            # title = get_title(u)
            if title:
                print(f"Title found in {u}: {title}")
                # 保存标题
                save_title(title, save_path = save_path+"/title.txt")
                title = title.split("深圳市")[0]
            else:
                print(f"Title not found in {u}.")
                continue

            save_pic(canvas_data, save_path = save_path, file_name = title)
            print(f"Canvas data saved in {save_path}/{title}.png")


def generate_all_url(first = 1, last = 5):
    url_list = []
    left_url = "https://www.szmc.net/shentieyunying/yunyingfuwu/meiyuekeliu/index"
    right_url = ".html"

    for i in range(first, last+1):
        if i == 1:
            url_list.append(f"{left_url}{right_url}")
        else:
            url_list.append(f"{left_url}_{i}{right_url}")

    return url_list


def crawl_all(first = 1, last = 5, save_path ="web_data"):
    url_list = generate_all_url(first, last)
    crawl_url_list(url_list, save_path = save_path)