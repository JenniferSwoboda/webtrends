try:
    import cPickle as pickle
except ImportError:
    import pickle
from datetime import timedelta
from pymongo import MongoClient
from pprint import pprint

class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        # if a client object is not passed
        # then try connecting to mongodb at the default localhost port
        self.client = MongoClient('localhost', 27017) if client is None else client
        # create collection to store cached webpages,
        # which is the equivalent of a table in a relational database
        #print self.client.database_names()
        # mongoexport --db cache --collection webpage --out webpage.json

        self.db = self.client.cache
        # WEBPAGE = GLOBAL
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())
        self.db.webpage_aut.create_index('timestamp', expireAfterSeconds=expires.total_seconds())
        self.db.webpage_design.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

        #self.db.webpage.drop()

    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, url):
        basic = self.db.webpage.find_one({'_id':url})
        if basic:
            return basic['title']
        else:
            raise KeyError(url + ' does not exist')

    def __getDate__(self, url):
        basic = self.db.webpage.find_one({'_id':url})
        if basic:
            return basic['timestamp_css']
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, title, base_url, alexa_global, categories):
        basic = {
            'title': title,
            'baseurl': base_url,
            'alexa': {
                'global': alexa_global
            },
            'categories': categories
        }
        self.db.webpage.update({'_id': base_url}, {'$set': basic}, upsert=True)

    def setcss(self, fonts, colors, background_colors, responsive, base_url, date):
        css = {
            'timestamp_css': {
                'time': date,
                'css': {
                    'fonts': fonts,
                    'colors': colors,
                    'bg_colors': background_colors,
                    'responsive': responsive
                }
            }
        }
        self.db.webpage.update({'_id': base_url}, {'$push': css}, upsert=True)


    def setbuiltwith(self, blogs, mobile_frameworks, font_scripts, web_servers, js_frameworks,
                     programming_lng, cms, ecommerce, web_frameworks, op_sys, cdn, video_players, character_encoding, site_elements,
                       analysis_tool, markup_lang, img_formats, base_url, date):
        built_with = {
            'timestamp_tech': {
                'time': date,
                'technology': {
                    'blogs': blogs,
                    'mobile_frameworks': mobile_frameworks,
                    'font_scripts': font_scripts,
                    'web_servers': web_servers,
                    'js_frameworks': js_frameworks,
                    'programming_lng': programming_lng,
                    'cms': cms,
                    'ecommerce': ecommerce,
                    'web_frameworks': web_frameworks,
                    'op_sys': op_sys,
                    'cdn': cdn,
                    'video_players': video_players,
                    'character_encoding': character_encoding,
                    'site_elements': site_elements,
                    'analysis_tool': analysis_tool,
                    'markup_lang': markup_lang,
                    'img_formats': img_formats
                }
            }
        }
        self.db.webpage.update({'_id': base_url}, {'$push': built_with}, upsert=True)



    def addbuiltwith(self, blogs, mobile_frameworks, font_scripts, web_servers, js_frameworks,
                     programming_lng, cms, ecommerce, web_frameworks, op_sys, cdn, video_players,
                     character_encoding, site_elements,
                     analysis_tool, markup_lang, img_formats, base_url, date):
        built_with = {
            'timestamp_tech': {
                'time': date,
                'technology': {
                    'blogs': blogs,
                    'mobile_frameworks': mobile_frameworks,
                    'font_scripts': font_scripts,
                    'web_servers': web_servers,
                    'js_frameworks': js_frameworks,
                    'programming_lng': programming_lng,
                    'cms': cms,
                    'ecommerce': ecommerce,
                    'web_frameworks': web_frameworks,
                    'op_sys': op_sys,
                    'cdn': cdn,
                    'video_players': video_players,
                    'character_encoding': character_encoding,
                    'site_elements': site_elements,
                    'analysis_tool': analysis_tool,
                    'markup_lang': markup_lang,
                    'img_formats': img_formats
                }
            }
        }
        self.db.webpage.update({'_id': base_url}, {'$set': built_with}, upsert=True)

    def clear(self):
        self.db.webpage.drop()

    def print_db(self):
        cursor = self.db.webpage.find({})
        for document in cursor:
            pprint(document)

    def print_item(self, cursor):
        for document in cursor:
            pprint(document)