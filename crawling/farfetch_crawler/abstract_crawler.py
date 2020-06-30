import os
import time
import re
import json

from PIL import Image
import requests
import urllib.request
from selenium import webdriver


class Clothes_Crawler:
    def __init__(self, folder_path="."):
        self.driver = self.getDriver()
        print("ancestor")

        self.num = 1

        self.category_id_dict = {
            "top": "01",
            "shirts": "02",
            "knit": "03",
            "pants": "04",
            "shoes": "05",
            "outer": "06",
            "bags": "07",
        }
        self.folder_path = folder_path

    def getDriver(self):
        # path = "/root/chrome_driver/chromedriver"
        path_window = r"/Users/seungsu/Desktop/YBIGTA/chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=2400,1080")
        # chrome_options.add_argument("headless")

        self.driver = webdriver.Chrome(path_window, options=chrome_options)
        self.driver.implicitly_wait(3)

        return self.driver

    # make db id
    def make_id(self, num, shop="10", category="00"):
        """
        shop     ; 29cm     : 11
        shop     ; musinsa  : 12
        shop     ; farfetch : 13

        category ; top      : 01
        category ; shirts   : 02
        category ; knit     : 03
        category ; pants    : 04
        category ; shoes    : 05
        category ; outer    : 06
        category ; bags     : 07
        """

        item_id = shop + category + str(num).rjust(6, "0")
        return item_id

    def getItemList(self):
        # make category page url

        # connect & get items url data

        # get simple item data

        # return item들 포함 리스트
        pass

    def crawl_item(self):
        # args : item_detail_url

        # result dictionary

        # connect

        # item info : (shop, product_id), brand, productname,

        # item detail info >> 디테일 정보 필요하다면 사용!

        # return detail_item_info : 세부 아이템 url에서 세부데이터 긁기
        pass

    def get_total_page(self):
        # return page
        pass

    # crawl items in the category and save as json file
    def crawl_category(self, m_category, s_category, page=1, save=False, path=None):

        """
        <Sub Category Crawler>
        m_category (str): main category
        s_category (str): sub category
        page       (int): how many page crawling   | Default : 1
        path       (str): save path                | Default : None
        save      (bool): save or not              | Default : False
        """
        pass

    # save as json!!
    def save_as_json(self, item_group, m_category, s_category, num, path=None):
        # save as json
        # set path
        if path == None:
            path = f"./{m_category}_{s_category}_{num}.json"
        else:
            path = path + f"/{m_category}_{s_category}_{num}.json"

        with open(path, "w", encoding="utf-8-sig") as make_file:
            json.dump(item_group, make_file, ensure_ascii=False, indent="\t")

    def crawl_AllCategory(self, categories=None, page=1, save=False, path=None):

        """
        <All Category Crawler>
        categories (list): main category            | Default : None (crawl all categories)
        page        (int): how many page crawling   | Default : 1
        path        (str): save path                | Default : None
        save       (bool): save or not              | Default : False
        """
        pass


class Downloader:
    def __init__(self):
        pass

    def make_directory(self, path):
        try:
            os.mkdir(f"./{path}/")
            print(f"\x1b[1;32m  {path} Directory is created!\x1b[1;m")
        except:
            print(f"\x1b[1;35m  {path} Directory exist!\x1b[1;m")

    def call_json(self):
        pass

    def read_json(self, file_name):
        with open(file_name, "r", encoding="utf-8-sig") as json_file:
            json_data = json.load(json_file)
        return json_data

    # size는 튜플로 (가로, 세로)
    def download(self, img_name, url, path=".", size=None):
        image = urllib.request.urlretrieve(url, f"{path}/{img_name}.png")

        if size != None:
            # image resize
            image = Image.open(f"{path}/{img_name}.png")
            resize_img = image.resize(size)
            resize_img.save(f"{path}/{img_name}.png")

    def download_all(self, files, path=".", size=None):
        """
        files  : file list
        """
        self.make_directory(path)

        for f in files:
            item_list = self.read_json(f)
            for item in item_list.values():
                item_img_url = item["img"]
                # img_name = item["category"] + "/" + item["id"]
                img_name = item["product_id"]
                print(f"{img_name}, {item_img_url}, {path} download!!")
                # self.download(img_name, item_img_url, path, size)


if __name__ == "__main__":
    d = Downloader()
    d.download_all(["./top_sleeveless_100.json", "./top_hoodie_100.json"], "./data/")
    print("end")
