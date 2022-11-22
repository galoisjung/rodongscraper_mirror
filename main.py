import pandas as pd
import scraping
import DAO

date_list = pd.date_range(start="2021-11-28", end="2021-12-30")
#date_list = pd.date_range(start="2022-11-02", end="2022-11-09")

mysql_instance = DAO.connection_mysql()
for date_pd in date_list:
    print(date_pd)
    date = str(date_pd.date())
    scraping_inst = scraping.Scraper(date)
    scraping_inst.initial_function()
    scraping_inst.run_scraper()
    news_list = scraping_inst.temp_result

    for i in news_list:
        DAO.add(i, mysql_instance)
