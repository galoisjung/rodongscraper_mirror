import hashlib
import json

import DAO
import news
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

class json2db:
    def __init__(self):
        self.result = Queue()
        self.mysql_instance = DAO.connection_mysql()
        #self.pool = ThreadPoolExecutor(max_workers=10)
        self.special = ["6dc472d7f246ab82b5a1987a7f0dcdb57a2f1a3751f581d486b8c50ca2e93b5f",
                        "6dc472d7f246ab82b5a1987a7f0dcdb57a2f1a3751f581d486b8c50ca2e93b5f",
                        "0e3062e48f44fc7d189557c5ddd20384736af36b743292ddb6b825e15caf4290",
                        "0e3062e48f44fc7d189557c5ddd20384736af36b743292ddb6b825e15caf4290",
                        "f24fa5c18215fce318683d1703b6ae0b523de7be3bc64035cb1c43997fc200ad",
                        "6b70f2eb5a51ee2a105f40b0eb39c4299615998045d46ac218ca752b22b16854",
                        "c840a9863fdbd83524992f793a6d63be4fa1c57bf1a17cb43cdd3b50864f52ac",
                        "bfa023c0ffd6b97213fe0926da364407c807be7375ab1b80aac335021294068a"]
        self.special_count = [0,0,0,0,0,0,0,0]
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
            #job = self.pool.submit(self.put_sql, j)
            #job.running()

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
        if news_instance.id in self.special:
            index = self.special.index(news_instance.id)

            if self.special_count[index] != 0:
                hash_seed = news_instance.title + news_instance.date
                news_instance.id = hashlib.sha256(hash_seed.encode('utf-8')).hexdigest()
                news_instance.author = i['author']
                news_instance.page = i['page']
                self.result.put(news_instance)
            else:
                self.special_count[index] += 1

    def put_sql(self, j):
        DAO.add(j, self.mysql_instance)
        return


if __name__ == '__main__':
    a = json2db()
    a.init_function()
