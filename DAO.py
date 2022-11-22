import json

import pymysql
import sqlite3
import scraping
import cryptography

with open('conf_DB.json') as f:
    config = json.load(f)


class connection_mysql:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user=config["SQL_ID"], passwd=config["SQL_PASSWORD"],
                                    db=config["DB"])
        self.query_1 = '''
            CREATE TABLE IF NOT EXISTS main_news(
            id VARCHAR(255) PRIMARY KEY,
            title LONGTEXT NOT NULL,
            author VARCHAR(255),
            `date` DATE NOT NULL,
            page INT,
            content LONGTEXT
            )
            '''
        self.query_2 = "INSERT INTO main_news(id, title, author, date, page, content) VALUES(%s,%s,%s,%s,%s,%s)"
        self.query_3 = "DELETE FROM main_news WHERE id=%s"
        self.query_4 = "SELECT COUNT(*) FROM main_news"


# class connection_sqlite:
#     def __init__(self, drink=False):
#         self.conn = sqlite3.connect("youtube.db")
#
#         if not drink:
#             self.query_1 = '''
#             CREATE TABLE IF NOT EXISTS nondrink(
#             id INT PRIMARY KEY,
#             title LONGTEXT NOT NULL,
#             author VARCHAR(255) NOT NULL,
#             `date` VARCHAR(255) NOT NULL,
#             `length` int NOT NULL,
#             resolution VARCHAR(225) NOT NULL,
#             keyword LONGTEXT)
#             '''
#             self.query_2 = "INSERT INTO nondrink(id, title, author, date, length, resolution,keyword)  VALUES(?,?,?,?,?,?,?)"
#             self.query_3 = "DELETE FROM nondrink WHERE id=?"
#             self.query_4 = "SELECT COUNT(*) FROM nondrink "
#         else:
#             self.query_1 = '''
#                 CREATE TABLE IF NOT EXISTS drink(
#                 id INT PRIMARY KEY,
#                 title LONGTEXT NOT NULL,
#                 author VARCHAR(255) NOT NULL,
#                 `date` VARCHAR(255) NOT NULL,
#                 resolution VARCHAR(225) NOT NULL,
#                 `length` int NOT NULL,
#                 keyword LONGTEXT)
#                 '''
#             self.query_2 = "INSERT INTO drink(id, title, author, date, length, resolution, keyword) VALUES(?,?,?,?,?,?,?)"
#             self.query_3 = "DELETE FROM drink WHERE id=?"
#             self.query_4 = "SELECT COUNT(*) FROM drink "
#

def add(news, con_instance):
    conn = con_instance.conn
    curs = conn.cursor()

    id = news.id
    title = news.title
    author = news.author
    date = news.date
    page = news.page
    content = news.content

    print(id, title, author, date, page)

    curs.execute(con_instance.query_1)
    conn.commit()

    curs.execute(con_instance.query_4)
    cnt = curs.fetchone()
    print("sql_count: " + str(cnt[0]))

    curs.execute(con_instance.query_3, (id,))
    conn.commit()

    curs.execute(con_instance.query_2, (id, title, author, date, page, content))
    conn.commit()


def update(id, con_instance, author):
    conn = con_instance.conn
    curs = conn.cursor()

    query = "UPDATE main_news SET author='{0}' WHERE id='{1}'".format(author, id)
    print(query)
    curs.execute(query)
    conn.commit()


def get(id, connection, dr):
    con_instance = connection()
    conn = con_instance.conn
    curs = conn.cursor()

    query = "SELECT title FROM {0} WHERE id == {1}".format(dr, str(id))

    curs.execute(query)
    conn.commit()

    result = curs.fetchone()

    conn.close()

    return result
