import os
import time
import re
import json
import time
import requests
import urllib.request
from selenium import webdriver
from argparse import ArgumentParser


# option
# parser = ArgumentParser()
# parser.add_argument("-p", "--num_page", type=int, help="number of page to crawl")
# parser.add_argument(
#     "-c",
#     "--all_category",
#     type=str,
#     nargs="+",
#     help="category which you want to crawl  >  상의  아우터  원피스  바지  스커트  가방  스니커즈  신발  시계  모자  스포츠용품  레그웨어속옷  안경  액세서리  디지털테크  생활취미예술  뷰티  반려동물  책음악티켓",
# )
# parser.add_argument(
#     "-f", "--folder_path", type=str, help="where to store crawled image"
# )


class o29cm_crawler:
    def __init__(self, folder_path="."):
        self.driver = self.getDriver()

        self.num = 1

        # 29cm shop url information
        self.top = {
            "short_sleeve": "01",
            "long_sleeve": "02",
            "pique_tshirts": "03",
            "sleeveless": "04",
            "sweat_shirts": "05",
            "hoodie": "06",
            "zipup": "07",
        }
        self.shirts = {"short_shirts": "01", "long_shirts": "02", "dress_shirts": "03"}
        self.pants = {
            "slacks": "01",
            "chino": "02",
            "short": "03",
            "cargo": "04",
            "denim": "05",
            "training": "06",
        }
        self.knit = {"crew": "01", "cardigan": "02", "turtle": "03", "vest": "04"}
        self.shoes = {
            "rain": "12",
            "sneakers": "01",
            "running": "09",
            "derby": "13",
            "boots": "05",
            "loafers": "03",
            "flipflop": "10",
            "sandle": "02",
        }
        self.outer = {
            "light_padding": "11",
            "fleece": "10",
            "blazer": "01",
            "trench_coat": "09",
            "trucker": "02",
            "coat": "06",
            "padding": "07",
            "robe": "04",
            "vest": "05",
        }
        self.bags = {"shoulder": "02", "tote": "05", "cross": "11", "backpack": "04"}
        self.medium_category = {
            "top": ("2551181", self.top),
            "shirts": ("2551021", self.shirts),
            "knit": ("2551041", self.knit),
            "pants": ("2551031", self.pants),
            "shoes": ("2551061", self.shoes),
            "outer": ("2551051", self.outer),
            "bags": ("2551071", self.bags),
        }
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
        chrome_options.add_argument("window-size=1920x1080")
        # chrome_options.add_argument("headless")

        self.driver = webdriver.Chrome(path_window, options=chrome_options)
        self.driver.implicitly_wait(3)

        return self.driver

    def getItemList(self, m_category, s_category, page="1"):
        # make category page url
        category_medium_code = self.medium_category[m_category][0]
        category_small_code = (
            category_medium_code + self.medium_category[m_category][1][s_category]
        )
        url = f"https://www.29cm.co.kr/shop/category/list?category_large_code=255100100&category_medium_code={category_medium_code}00&category_small_code={category_small_code}&sort=latest&page={str(page)}&brand=&min_price=&max_price=&count=50"

        # connect & get items url data
        self.driver.get(url)
        ul = self.driver.find_element_by_css_selector("ul.prd_section")
        all_items = ul.find_elements_by_css_selector("a.prd_b_area")
        items = []

        # get simple item data
        for a in all_items:
            # item detail url
            item_url = a.get_attribute("href")

            # item image data >> 진짜 간단히 아이템 사진만 긁을 때
            # item_img = (
            #     a.find_element_by_css_selector("div.imgbx")
            #     .find_element_by_css_selector("img.b-lazy")
            #     .get_attribute("src")
            # )
            # img = item_img

            # item brand, name
            # item_brand = a.find_element_by_css_selector("div.brand").text
            # item_name = a.find_element_by_css_selector("div.name").text

            items.append({"href": item_url})
            # "brand":item_brand, "name":item_name, "img":img,

        return items

    def crawl_item(self, item_detail_url):
        time.sleep(1)
        # result dictionary
        detail_item_info = {}

        # connect
        self.driver.get(item_detail_url)

        # item info : (shop, product_id), brand, productname,
        detail_item = self.driver.find_element_by_css_selector("div.detail_item")
        detail_item_info["shop"] = "29cm"
        detail_item_info["brand"] = detail_item.find_element_by_css_selector(
            "h1.kor"
        ).text
        # detail_item_info["brand"] = detail_item.find_element_by_css_selector("h1.eng").text
        detail_item_info["product"] = detail_item.find_element_by_css_selector(
            "div.name"
        ).text
        detail_item_info["product_id"] = self.driver.find_element_by_css_selector(
            "em.dsc"
        ).text
        # url
        detail_item_info["url"] = item_detail_url
        # item image url
        detail_item_img = detail_item.find_element_by_css_selector(
            "img.b-lazy.b-loaded"
        ).get_attribute("src")
        detail_item_info["img"] = detail_item_img

        # item detail info >> 디테일 정보 필요하다면 사용!
        # infos = self.driver.find_element_by_css_selector(
        #     "div.item_info"
        # ).find_elements_by_css_selector("tr")
        # for row in infos:
        #     key = (
        #         row.find_element_by_css_selector("th")
        #         .find_element_by_css_selector("div")
        #         .text
        #     )
        #     value = (
        #         row.find_element_by_css_selector("td")
        #         .find_element_by_css_selector("div")
        #         .text
        #     )
        #     detail_item_info[key] = value

        return detail_item_info

    # make db id
    def make_id(self, num, shop="11", category="00"):
        """
        shop     ; 11 : 29cm
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

    def get_total_page(self, m_category, s_category, page):
        # make category page url
        category_medium_code = self.medium_category[m_category][0]
        category_small_code = (
            category_medium_code + self.medium_category[m_category][1][s_category]
        )

        url = f"https://www.29cm.co.kr/shop/category/list?category_large_code=255100100&category_medium_code={category_medium_code}00&category_small_code={category_small_code}&sort=latest&page=1&brand=&min_price=&max_price=&count=50"
        self.driver.get(url)
        page_div = self.driver.find_element_by_css_selector("div.custom-pagination")
        page_list = page_div.find_elements_by_css_selector("span")
        total_page = page_list[-2].find_element_by_css_selector("a").text

        if int(page) > int(total_page):
            page = int(total_page)

        return page

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

        # result dictionary (json)
        item_group = dict()

        # page
        for p in range(1, int(page) + 1):
            # itemList in page
            itemList = self.getItemList(m_category, s_category, p)

            # make item to dict
            for item in itemList:
                item_id = self.make_id(
                    self.num, "11", self.category_id_dict[m_category]
                )
                item_group[item_id] = self.crawl_item(item["href"])
                item_group[item_id]["id"] = item_id
                item_group[item_id]["category"] = m_category
                item_group[item_id]["sub_category"] = s_category

                self.num += 1

            # if p % 5 == 0:
            print(f"{p}  crawled")

        # save as json
        if save:
            # set path
            if path == None:
                path = f"./{m_category}_{s_category}_{page*50}.json"
            else:
                path = path + f"/{m_category}_{s_category}_{page*50}.json"

            with open(path, "w", encoding="utf-8-sig") as make_file:
                json.dump(item_group, make_file, ensure_ascii=False, indent="\t")

        return item_group

    def crawl_AllCategory(self, categories=None, page=1, save=False, path=None):

        """
        <All Category Crawler>
        categories (list): main category            | Default : None (crawl all categories)
        page        (int): how many page crawling   | Default : 1
        path        (str): save path                | Default : None
        save       (bool): save or not              | Default : False
        """

        if categories == None:
            for m_cat_name, s_category in self.medium_category.items():
                self.num = 1
                for s_cat_name in s_category[1].keys():
                    page = self.get_total_page(m_cat_name, s_cat_name, page)
                    self.crawl_category(
                        m_cat_name, s_cat_name, page, path=path, save=save
                    )
                    print(f"\x1b[1;32mCOMPLETE\x1b[1;m\t{m_cat_name} > {s_cat_name}")
        else:
            for m_cat_name in categories:
                self.num = 1
                for s_cat_name in self.medium_category[m_cat_name][1].keys():
                    page = self.get_total_page(m_cat_name, s_cat_name, page)
                    self.crawl_category(
                        m_cat_name, s_cat_name, page, path=path, save=save
                    )
                    print(f"\x1b[1;32mCOMPLETE\x1b[1;m\t{m_cat_name} > {s_cat_name}")


if __name__ == "__main__":

    crawler = o29cm_crawler()

    crawler.crawl_AllCategory(["top"], 1, True)
