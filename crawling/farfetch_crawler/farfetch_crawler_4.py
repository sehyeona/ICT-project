import os
import time
import re
import json
import time
import requests
import urllib.request
from selenium import webdriver
from argparse import ArgumentParser
import abstract_crawler
from tqdm import tqdm


class farfetch_crawler(abstract_crawler.Clothes_Crawler):
    def __init__(self):
        super().__init__()

        self.category_name = [
            "knit",
            "denim",
            "shirts",
            "shorts",
            "suit",
            "jacket",
            "coat",
            "t-shirt",
            "pants",
            "polo-shirt",
        ]

        self.category_id = {
            "knit": "01",
            "denim": "02",
            "shirts": "01",
            "shorts": "02",
            "suit": "04",
            "jacket": "01",
            "coat": "04",
            "t-shirts": "01",
            "pants": "02",
            "polo-shirt": "01"
        }

        self.category_url_list = {
            "knit": {
                "category": "knit",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136334",
            },
            "denim": {
                "category": "denim",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136337",
            },
            "shirts": {
                "category": "shirts",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136331",
            },
            "shorts": {
                "category": "shorts",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136339",
            },
            "suit": {
                "category": "suit",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136340",
            },
            "jacket": {
                "category": "jacket",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136335",
            },
            "coat": {
                "category": "coat",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136336",
            },
            "t-shirt": {
                "category": "t-shirt",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136332",
            },
            "pants": {
                "category": "pants",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136338",
            },
            "polo-shirt": {
                "category": "polo-shirt",
                "url": "https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx?view=180&category=136333",
            },
        }

    def getItemList(self, sub_category, page=1):
        # self.category_url_list
        itemList_url = (
            self.category_url_list[sub_category]["url"][:63]
            + f"page={str(page)}&"
            + self.category_url_list[sub_category]["url"][63:]
        )
        self.driver.get(itemList_url)
        items = []
        time.sleep(2)
        ul = self.driver.find_element_by_css_selector("ul._53c8ee")
        all_items = ul.find_elements_by_css_selector("li._c29d78._d85b45")
        for item in all_items:
            box = item.find_element_by_css_selector("div._8eb9f8._a57b85")

            item_url = item.find_element_by_css_selector("a").get_attribute("href")
            # img = item.find_element_by_css_selector("img._fc8ffc").get_attribute("src")
            item_brand = box.find_element_by_css_selector("h3._346238").text
            item_name = box.find_element_by_css_selector("p._d85b45").text

            items.append({"brand": item_brand, "name": item_name, "href": item_url})

        return items

    def crawl_item(self, item_detail_url):
        # 데이터 저장 dict
        detail_item_info = {}

        # 접속
        self.driver.get(item_detail_url)
        time.sleep(2)
        # soup = bs(self.driver.page_source, "html.parser")

        # 기본정보
        # detail_item = self.driver.find_element_by_css_selector("div._9d3f24._da3196")
        basic_info = self.driver.find_element_by_css_selector("div._c40757")

        try:
            img_list = self.driver.find_element_by_css_selector(
                "div._cc7da7"
            ).find_elements_by_css_selector("img._f3a89c")
        except:
            img_list = self.driver.find_element_by_css_selector(
                "div._8f4767"
            ).find_elements_by_css_selector("img._167ff2._2ca15d")

        category_box = self.driver.find_element_by_css_selector("ol._4e9dce")

        detail_item_info["shop"] = "farfetch"
        detail_item_info["brand"] = basic_info.find_element_by_css_selector(
            "span._e87472._346238._e4b5ec"
        ).text
        detail_item_info["product"] = basic_info.find_element_by_css_selector(
            "span._d85b45._d85b45._1851d6"
        ).text
        detail_item_info["product_id"] = basic_info.find_element_by_css_selector(
            "span._d85b45._d85b45._1851d6"
        ).get_attribute("data-attribute")
        detail_item_info["url"] = item_detail_url
        detail_item_info["sub_category"] = (
            category_box.find_elements_by_css_selector("li._9d7c74")[-1]
            .find_element_by_css_selector("span")
            .text
        )
        # detail_item_info["category"] =
        # detail_item_info["id"] =

        # 이미지url
        detail_item_img = []
        for img in img_list:
            detail_item_img.append(img.get_attribute("src"))
        detail_item_info["img"] = detail_item_img

        detail_item_info
        # 상세정보
        # infos = self.driver.find_element_by_css_selector("div._9d3f24._da3196").find_elements_by_css_selector("div._4919a3._da3196")
        # for row in infos:
        #     pass
        return detail_item_info

    def crawl_category(self, sub_category, page, path=None, save=False):
        # 아이템 dict을 저장할 dict
        item_group = dict()
        num = 1

        # page 별
        for p in range(1, int(page + 1)):
            # 페이지 item리스트 뽑기
            itemList = self.getItemList(sub_category, p)
            print(f"{sub_category} > {p} page")
            # 개별 아이템 json화
            for item in tqdm(itemList):
                try:
                    item_id = self.make_id(num, "10", self.category_id[sub_category])
                    a = self.crawl_item(item["href"])
                    item_group[item_id] = a
                    num += 1
                except:
                    print("pass")
                    continue

            # json으로 저장
            if save == True:
                # path 설정
                if path == None:
                    path = f"/home/ubuntu/data/ff_{sub_category}.json"
                else:
                    path = path + "~/ff_{sub_category}_{p}.json"
                with open(path, "w", encoding="utf-8") as make_file:
                    json.dump(item_group, make_file, ensure_ascii=False, indent="\t")
        return item_group


if __name__ == "__main__":
    crawler = farfetch_crawler()

    #crawler.crawl_category("knit", page=63, save=True)
    #crawler.crawl_category("denim", page=18, save=True)
    #crawler.crawl_category("shirts", page=42, save=True)
    crawler.crawl_category("shorts", page=15, save=True)
    #crawler.crawl_category("jacket", page=51, save=True)
    #crawler.crawl_category("coat", page=10, save=True)
    #crawler.crawl_category("t-shirt", page=58, save=True)
    #crawler.crawl_category("pants", page=41, save=True)
    #crawler.crawl_category("polo-shirt", page=17, save=True)
