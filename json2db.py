import hashlib
import json

import DAO
import news

list_of_date = ["2020-09-22", "2020-09-23", "2020-09-24"]

news_instance = news.news()
mysql_instance = DAO.connection_mysql()

with open("main_news_mirror.json", "r") as f:
    whole_news = json.load(f)

result = list()

for i in whole_news:
    news_instance = news.news()
    if i['date'] in list_of_date:
        news_instance.date = i['date']
        news_instance.title = i['title']
        news_instance.id = hashlib.sha256(i["title"].encode('utf-8')).hexdigest()
        news_instance.author = i['author']
        news_instance.date = i['date']
        news_instance.page = i['page']
        news_instance.content = i['content']
        result.append(news_instance)

for i in result:
    DAO.add(i ,mysql_instance)