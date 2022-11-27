import pandas as pd

import scraping
import DAO

mysql_instance = DAO.connection_mysql()

a = DAO.get_all(mysql_instance,"main_news_mirror_fix")

id_list = [i[0] for i in a]

for i in range(7439,8000):
    print(i)
    scraping_inst = scraping.Scraper(i)
    scraping_inst.initial_function()
    scraping_inst.run_scraper()
    news_list = scraping_inst.temp_result

    for j in news_list:
        if j.id not in id_list:
          DAO.add(j,mysql_instance)