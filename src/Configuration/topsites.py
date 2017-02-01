from bs4 import BeautifulSoup
import requests
from math import ceil
from src.Configuration import mongocache
from src.Crawler import crawler

BASE_URL='http://www.alexa.com/topsites/'
#BASE_URL='http://www.alexa.com/topsites/countries;%d/%s'
#BASE_URL='http://www.alexa.com/topsites/category;%d/%s'

COUNTRY_CODE = 'Top/Arts/Design'
TOP_N = 100

if __name__ == '__main__':
    country_code = COUNTRY_CODE
    number = int(TOP_N)
    delimiter = ' '
    mongo = mongocache.MongoCache()

    page_numbers = int(ceil(number/25.0))
    for page_num in range(0, page_numbers):
        # country
        #response = requests.get(BASE_URL % (page_num, country_code))

        # global
        url = BASE_URL + 'global;' + str(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        bullets = soup.find_all('li', {'class':'site-listing'})

        for bullet in bullets:
            rank = bullet.div.contents[0]
            site = bullet.p.a.contents[0]
            base_url = crawler.Crawler.get_base_URL(site)
            #categories = crawler.Crawler.get_category(base_url)
            alexa = crawler.Crawler.popularity_rank(base_url)

            mongo.__setitem__('', base_url, alexa, '')

            print('%s%s%s' % (rank, delimiter, base_url))
    mongo.print_db()
