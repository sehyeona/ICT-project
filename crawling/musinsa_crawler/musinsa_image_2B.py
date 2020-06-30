import os
import time
import re
from PIL import Image
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from argparse import ArgumentParser


# option
parser = ArgumentParser()
parser.add_argument("-p", "--num_page", type=int, help="number of page to crawl")
parser.add_argument(
    "-c",
    "--all_category",
    type=str,
    nargs="+",
    help="category which you want to crawl  >  상의  아우터  원피스  바지  스커트  가방  스니커즈  신발  시계  모자  스포츠용품  레그웨어속옷  안경  액세서리  디지털테크  생활취미예술  뷰티  반려동물  책음악티켓",
)
parser.add_argument(
    "-f", "--folder_path", type=str, help="where to store crawled image"
)


class musinsa_crawler:
    def __init__(self, folder_path="."):
        self.category = self.get_category_data_B()
        self.folder_path = folder_path

    def get_category_data_B(self):
        url = "https://store.musinsa.com/app/"
        html = requests.get(url).text
        bsObj = bs(html, "html.parser")
        navs = bsObj.find_all("div", {"class": "nav_category"})[1:]
        category = {}
        for nav in navs:
            cat = {}
            big = nav.find("div", {"class": "nav_menu_title"})
            big_cat_name = (
                big.find("strong", {"class": "title"}).text.replace("/", "").strip(" ")
            )
            ll = nav.find("div", {"class": "item_sub_menu"})
            uls = ll.find_all("ul")
            for ul in uls:
                al = ul.find_all("li")
                for a in al:
                    m = a.find("a")
                    h = m["href"]
                    exp = re.compile("[가-힣\s/]*")
                    title = (
                        exp.findall(m.text)[0]
                        .strip("\r\n\t")
                        .replace("/", " ")
                        .strip(" ")
                    )
                    cat[title] = h
            category[big_cat_name] = cat

        return category

    def check_directory(self, category_name):
        """
        category_name (str): Category name
        """
        try:
            os.mkdir(f"{self.folder_path}/{category_name}/")
            print(f"\x1b[1;32m  {category_name} Directory is created!\x1b[1;m")
        except:
            print(f"\x1b[1;35m  {category_name} Directory exist!\x1b[1;m")

    def getBSobj(self, category_id, page=1):
        """
        <Get BS object with fake header>
        page        (int): how many page crawling   | Default : 1
        category_id (str): Sub Category ID
        """
        url = f"https://store.musinsa.com/app/items/lists/{category_id}/?category=&d_cat_cd={category_id}&u_cat_cd=&brand=&sort=pop&sub_sort=&display_cnt=90&page={str(page)}&page_kind=category&list_kind=small&free_dlv=&ex_soldout=&sale_goods=&exclusive_yn=&price=&color=&a_cat_cd=&sex=&size=&tag=&popup=&brand_favorite_yn=&goods_favorite_yn=&blf_yn=&campaign_yn=&price1=&price2=&brand_favorite=&goods_favorite=&chk_exclusive=&chk_sale=&chk_soldout="
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        html = session.get(url, headers=headers).content
        bsObj = bs(html, "html.parser")
        return bsObj

    # 한 페이지 크롤러
    def crawl_page(self, bsObj, category_name, sub_name):
        """
        <Page Crawler>
        bsObj       (bs4Obj): BS object that contains page where you want to crawl
        category_name  (str): Category name
        sub_name       (int): Sub Category name
        """
        body = bsObj.find("ul", {"class": "snap-article-list"})
        all_items = body.find_all("li", {"class": "li_box"})
        for li in all_items:
            a = li.find("a", {"class": "img-block"})
            id = a["href"].lstrip("/app/product/detail/").rstrip("/0")
            img = "http:" + a.find("img")["data-original"]
            # img = "http:" + a.find("img")["data-original"][:-7] + "500.jpg"
            image = urllib.request.urlretrieve(
                img,
                f"{self.folder_path}/{category_name}/{category_name}_{sub_name}_{id}.png",
            )
            # image resize
            image = Image.open(
                f"{self.folder_path}/{category_name}/{category_name}_{sub_name}_{id}.png"
            )
            resize_img = image.resize((128, 128))
            resize_img.save(
                f"{self.folder_path}/{category_name}/{category_name}_{sub_name}_{id}.png"
            )

    # sub category 별 크롤러
    def crawl_SubCategory(self, main, sub, page=1):
        """
        <Sub Category Crawler>
        main (str): main category
        sub  (str): sub category
        page (int): how many page crawling   | Default : 1
        """
        category_id = self.category[main][sub].lstrip(
            "https://store.musinsa.com/app/items/lists/"
        )

        bsObj = self.getBSobj(page=1, category_id=category_id)
        total_page = bsObj.find("span", {"class": "totalPagingNum"}).text.strip(" ")
        if page > int(total_page):
            page = int(total_page)

        for p in range(1, int(page + 1)):
            print(f"CRAWLING\t{main}\t>\t{sub} \t\t page = {p}")
            bsObj = self.getBSobj(page=p, category_id=category_id)
            self.crawl_page(bsObj, category_name=main, sub_name=sub)
            rand_time = 1
            time.sleep(rand_time)

    def crawl_AllCategory(self, categories=None, page=1):
        """
        <All Category Crawler>
        categories (list): main category            | Default : None (crawl all categories)
        page        (int): how many page crawling   | Default : 1
        """
        if categories == None:
            for category_name, contents in self.category.items():
                self.check_directory(category_name=category_name)
                for sub_category_name in contents.keys():
                    self.crawl_SubCategory(
                        main=category_name, sub=sub_category_name, page=page
                    )
                    print(
                        f"\x1b[1;32mCOMPLETE\x1b[1;m\t{category_name} > {sub_category_name}"
                    )
        else:
            for category_name in categories:
                self.check_directory(category_name=category_name)
                for sub_category_name in self.category[category_name].keys():
                    self.crawl_SubCategory(
                        main=category_name, sub=sub_category_name, page=page
                    )
                    print(
                        f"\x1b[1;32mCOMPLETE\x1b[1;m\t{category_name} > {sub_category_name}"
                    )


if __name__ == "__main__":
    args = parser.parse_args()

    crawler = musinsa_crawler(args.folder_path)

    crawler.crawl_AllCategory(
        categories=args.all_category, page=args.num_page,
    )
