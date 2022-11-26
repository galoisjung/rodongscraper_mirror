import hashlib
import json

import DAO
import news
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


class json2db:
    def __init__(self):
        self.result = Queue()
        self.mysql_instance = DAO.connection_sqlite()
        # self.pool = ThreadPoolExecutor(max_workers=1)

    def init_function(self):
        with open("/content/drive/MyDrive/main_news_mirror.json", "r") as f:
            whole_news = json.load(f)
        for j, i in enumerate(whole_news):
            news_instance = news.news()
            print(str(j) + "/" + str(len(whole_news)))
            self.making_instance(news_instance, i)

        print(self.result.empty())
        while not self.result.empty():
            j = self.result.get(timeout=3)
            self.put_sql(j)
            # job = self.pool.submit(self.put_sql, j)
            # job.running()

    # news_instance.date = i['date']
    # news_instance.title = i['title']
    # news_instance.content = i['content']
    # if len(news_instance.content.strip()) != 0:
    #     hash_seed = news_instance.title + news_instance.content.splitlines()[0] + news_instance.date
    # else:
    #     hash_seed = news_instance.title
    # news_instance.id = hashlib.sha256(hash_seed.encode('utf-8')).hexdigest()
    # news_instance.author = i['author']
    # news_instance.date = i['date']
    # news_instance.page = i['page']
    # if news_instance.id in result:
    #     print("damn")
    #     print(news_instance.date)
    #     print(news_instance.id)
    #     print(news_instance.title)
    #     print(news_instance.content)
    # else:
    #     result.append(news_instance.id)
    # if j == 0 or DAO.get(news_instance.id, mysql_instance, "main_news_mirror_fix") == None:
    #     DAO.add(news_instance, mysql_instance)

    # for i in result:
    # DAO.add(i ,mysql_instance)

    def making_instance(self, news_instance, i):
        news_instance.date = i['date']
        news_instance.title = i['title']
        news_instance.content = i['content']
        if len(news_instance.content.strip()) != 0:
            hash_seed = news_instance.title + news_instance.content.splitlines()[0] + news_instance.date
        else:
            hash_seed = news_instance.title
        news_instance.id = hashlib.sha256(hash_seed.encode('utf-8')).hexdigest()
        news_instance.author = i['author']
        news_instance.date = i['date']
        news_instance.page = i['page']
        self.result.put(news_instance)

    def put_sql(self, j):
        DAO.add(j, self.mysql_instance)
        return


if __name__ == '__main__':
    a = json2db()
    a.init_function()
