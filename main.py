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
        DAO.add(j, mysql_instance)

