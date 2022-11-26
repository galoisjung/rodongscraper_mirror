import pandas as pd

import scraping
import DAO

mysql_instance = DAO.connection_mysql()

for i in range(1000):
    print(i)
    scraping_inst = scraping.Scraper(i)
    scraping_inst.initial_function()
    scraping_inst.run_scraper()
    news_list = scraping_inst.temp_result

    for j in news_list:
        if DAO.get(j.id,mysql_instance,"main_news_mirror_fix") == None:
            DAO.add(j, mysql_instance)

