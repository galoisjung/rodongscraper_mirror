import multiprocessing
import random
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import hashlib

import bs4 as bs4
import requests
import re
import news


class Scraper:

    def __init__(self, num):
        self.date = num
        self.seed_url = "https://kcnawatch.org/"
        self.rodong_url = self.seed_url + "wp-admin/admin-ajax.php?action=get_cat_by_source&die=true&from=0&to=10&sort=&id=189661"
        self.pool = ThreadPoolExecutor(max_workers=5)
        self.scraped_ids = set([])
        self.news_queue = Queue()
        self.temp_result = list()
        self.size_of_news = 10

    def initial_function(self):
        resp = requests.get(self.rodong_url)
        dom = bs4.BeautifulSoup(resp.content, "lxml")
        news_list = dom.select(".article-desc")
        resp.close()
        for i in news_list:
            self.news_queue.put(i)

    def run_scraper(self):
        while len(self.temp_result) != 10:
            try:
                news_inst = news.news()
                news_chunk = self.news_queue.get(timeout=3)
                news_inst.title = news_chunk.select("a")[0].text
                news_inst.id = hashlib.sha256(news_inst.title.encode('utf-8')).hexdigest()

                if news_inst.id not in self.scraped_ids:
                    self.site_scraper(news_chunk, news_inst)
                    full_content_url = news_chunk.select("a")[0]['href']
                    print("Scraping URL {}".format(full_content_url))
                    self.scraped_ids.add(news_inst.id)

                    job = self.pool.submit(self.content_crop, news_inst, full_content_url)
                    job.add_done_callback(self.post_scrape_callback)

            except Exception as e:
                print(e)
                continue

    def site_scraper(self, news_chunk, news_inst):
        date = news_chunk.select(".articled-date > span")[0].text
        datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
        news_inst.page = -1
        if len(news_chunk.select(".col-sm-3 >p")) != 0:
            news_inst.author = news_chunk.select(".col-sm-3 >p")[0].text
        elif len(news_chunk.select(".col-sm-2 >p")) != 0:
            news_inst.author = news_chunk.select(".col-sm-2 >p")[0].text
        else:
            news_inst.author = ""

    def post_scrape_callback(self, news_inst):
        news_inst = news_inst.result()
        self.temp_result.append(news_inst)
        print(len(self.temp_result), "/", self.number_of_news)

    def content_crop(self, news_inst, url):
        content = str()
        time.sleep(random.uniform(2, 3))
        resp = requests.get(url)
        print(url)
        dom = bs4.BeautifulSoup(resp.content, "lxml")
        paragraphs_list = dom.select(".ArticleContent")
        for paragraph in paragraphs_list:
            content += paragraph.text + "\n"
        resp.close()
        news_inst.content = content

        return news_inst
