from folderScanner.scanner import all_pics
from ocr.OCR import pic_recognition, pair_result, sort_result

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

from webCrawler.CrawlSZMC import get_canvas, get_url_list, crawl_url_list


def test():
    url = "https://www.szmc.net/shentieyunying/yunyingfuwu/meiyuekeliu/202205/98432.html"
    get_canvas(url)
    pass


def test_ocr():
    # file_list = all_pics("test_data")
    file_list = ['test_data/2018年07月.png', 'test_data/2020年07月.png', 'test_data/2022年9月.png']
    print(file_list)
    for file_name in file_list:
        print("-" * 10)
        print(file_name)
        ocr_result = pic_recognition(file_name, save_path = "test_data/ocr_result.txt")
        # for element in ocr_result:
        #     print(element[1], ":")
        #     print(element[0][0][0], element[0][0][1])
        #     print(element[0][1][0], element[0][1][1])
        #     print(element[0][2][0], element[0][2][1])
        #     print(element[0][3][0], element[0][3][1])
        sorted_result = sort_result(ocr_result)
        print(sorted_result)
        print("-"*10)
        paired_result = pair_result(sorted_result)
        print(paired_result)

def test_crawler():
    # 使用Chrome浏览器
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 2000)  # 足够大的浏览器窗口

    # 打开页面
    url = "https://www.szmc.net/shentieyunying/yunyingfuwu/meiyuekeliu/202205/98432.html"
    driver.get(url)

    # 等待页面加载完成
    time.sleep(5)  # 等待一定时间，确保JavaScript渲染完成

    # 获取canvas元素
    canvas = driver.find_element(By.ID, "canvasDiv").find_element(By.TAG_NAME, "canvas")

    # 将canvas保存为图片
    canvas_data = canvas.screenshot_as_png  # 获取canvas的截图

    # 保存为文件
    with open("test_data/metro_chart.png", "wb") as f:
        f.write(canvas_data)

    # 关闭浏览器
    driver.quit()


def test_get_url_list():
    url = "https://www.szmc.net/shentieyunying/yunyingfuwu/meiyuekeliu/index.html"
    print(get_url_list(url))


def test_crawl_list():
    n = 5 # 页数
    url_list = []
    left_url = "https://www.szmc.net/shentieyunying/yunyingfuwu/meiyuekeliu/index"
    right_url = ".html"

    for i in range(1, n+1):
        if i == 1:
            url_list.append(f"{left_url}{right_url}")
        else:
            url_list.append(f"{left_url}_{i}{right_url}")

    crawl_url_list(url_list, save_path ="test_data")