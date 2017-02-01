from src.Crawler import cssCrawler, compareData, crawler
from src.Configuration import mongocache

import datetime
import time

mongo = mongocache.MongoCache()
cursor = mongo.db.webpage.find({})
#cursor = mongo.db.webpage_aut.find({})
#cursor = mongo.db.webpage_design.find({})
urls = []


for key in cursor:
    urls.append(key['_id'])

visited = set()

logfile = open('crawled_list', 'a')
timestamp = str(datetime.datetime.now())


class Main:

    def __init__(self):

        #mongo.db.webpage.find_one_and_delete({'_id': 'Onlinesbi.com'})

        self.start()
        #mongo.print_db()


    def start(self):
        #count = 0
        for url in urls:


            base_url = crawler.Crawler.get_base_URL(url)
            print base_url
            date_exists = compareData.CompareData.compare_dates(base_url, 'timestamp_tech')

            if date_exists is False:
                print "url  " + url
                crawler.Crawler.crawl_data(url)
                time.sleep(10)

            date_exists2 = compareData.CompareData.compare_dates(base_url, 'timestamp_css')
            if date_exists2 is False:
                print "url  " + url
                cssCrawler.CssCrawler.craw_css_data(url)
            else:
                print "Already crawled"

            cursor = mongo.db.webpage.find({'_id': base_url})
            mongo.print_item(cursor)



app = Main()
