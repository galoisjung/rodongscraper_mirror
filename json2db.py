import hashlib
import json

import DAO
import news

news_instance = news.news()
mysql_instance = DAO.connection_mysql()

with open("main_news_mirror.json", "r") as f:
    whole_news = json.load(f)

result = list()

for j, i in enumerate(whole_news):
    print(str(j) + "/" + str(len(whole_news)))
    news_instance = news.news()
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
    if news_instance.id in result:
        print("damn")
        print(news_instance.date)
        print(news_instance.id)
        print(news_instance.title)
        print(news_instance.content)
    else:
        result.append(news_instance.id)

    if j == 0 or DAO.get(news_instance.id, mysql_instance, "main_news_mirror_fix") == None:
        DAO.add(news_instance, mysql_instance)

# for i in result:
# DAO.add(i ,mysql_instance)
