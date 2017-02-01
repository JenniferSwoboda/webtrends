import urllib2
import whois
import builtwith
import lxml.html
import sys
import urllib
from urlparse import urlparse
import exceptions
import bs4
import requests
import json
from src.Configuration import printer, download, mongocache
from src.Crawler import compareData

logfile = open('errors_crawler', 'w')
mongo = mongocache.MongoCache()

class Crawler:
    def __init__(self):
        pass


    @staticmethod
    def crawl_data(url):
        """
        Crawl the technical data of a website and save it in mongo DB
        :param url: URL of the Website to crawl
        :return:
        """

        # --------- Get Base URL --------- #
        base_url = Crawler.get_base_URL(url)
        url = 'http://' + base_url

        # --------- Download HTML --------- #
        D = download.Downloader()
        html = D(url)

        printer.Printer.prettifyOutput("downloads")
        print (base_url)
        # html = Crawler.fix_html(html, url)

        # --------- GET TITLE OF WEBSITE --------- #
        title = Crawler.extract_data_by_css(html, 'title', base_url)

        # --------- GET TECH DATA --------- #
        printer.Printer.prettifyOutput("Built With")
        Crawler.builtwith_function(url, base_url)

        # --------- GET CATEGORY OF WEBSITE --------- #
        printer.Printer.prettifyOutput("CATEGORY")
        categories = Crawler.get_category(base_url)
        print categories

        # --------- GET ALEXA RANK  --------- #
        printer.Printer.prettifyOutput("Alexa Rank")
        alexa = Crawler.popularity_rank(base_url)

        # --------- SET DATA INTO DB --------- #
        mongo.__setitem__(title, base_url, alexa, categories)
        #mongo.print_db()

    @staticmethod
    def get_base_URL(full_url):
        """
        Get the basic URL, for example: google.com
        :param full_url: for example https://www.google.com
        :return: google.com
        """
        try:
            parsed_url = urlparse(full_url)
            base_url = parsed_url.geturl().replace('https://', '').replace('www.', '').replace('http://', '')
            return base_url
        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: get_base_URL " + " URL: " + full_url + ", " + "\n")
        finally:
            pass

    # Get the owner of the url
    @staticmethod
    def whois_function(url):
        """
        Get the owner of the URL
        :param url: URL of website
        :return: WHO IS
        """
        try:
            return whois.whois(url)
        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: whois_function " + " URL: " + url + ", " + "\n")
        finally:
            pass

    @staticmethod
    def w3tech_function(url, base_url):
        """
        get w3Tech Data
        :param url: for example https://google.com
        :param base_url: for example google.com
        :return: tech data
        """
        try:
            w3tech = {}
            w3tech_url = 'https://w3techs.com/sites/info/' + base_url
            cat = ''
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.get(w3tech_url, headers=headers)
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.content, "lxml")
                headings = soup.findAll("div", attrs={"class": "si_h"})

                for h in headings:
                    print h
                    add_items = []
                    count = 0
                    sib = h.nextSibling
                    while "si_h" not in str(sib):
                        sib = sib.nextSibling

                        categories = h.findAll('a')
                        for cat in categories:
                            cat = cat.text
                        try:
                            items = sib.findAll('a')
                        except:
                            break
                        for item in items:
                            add_items.append(item.text)

                        sib = sib.nextSibling
                        w3tech[cat] = add_items
                        print w3tech[cat]

            return w3tech
        except:
            w3tech = {}
            return w3tech
            pass

    # Get the technology and frameworks and webservers
    @staticmethod
    def builtwith_function(url, base_url):
        """
        Get the technology from builtwith and get date from w3Tech
        :param url: full url
        :param base_url: base_url
        :return: tech data
        """
        try:
            builtw = builtwith.parse(url)
            print builtwith
            w3tech = Crawler.w3tech_function(url, base_url)
            if w3tech == {} or len(w3tech) == 0:
                sys.exit()
            print "BUILTWITH"
            print builtw
            print "W3tech"
            print w3tech
            blogs = []
            mobile_frameworks = []
            font_scripts = []
            web_servers = []
            js_frameworks = []
            programming_lng = []
            cms = []
            ecommerce = []
            web_frameworks = []
            op_sys = []
            cdn = []
            video_players = []
            character_encoding = []
            site_elements = []
            analysis_tool = []
            markup_lang = []
            img_formats = []


            for w in w3tech:
                print w
                if w in 'Operating System':
                    for item in w3tech[w]:
                        op_sys.append(item)
                if w in 'Client-side Programming Language':
                    for item in w3tech[w]:
                        programming_lng.append(item)
                if w in 'Server-side Programming Language':
                    for item in w3tech[w]:
                        programming_lng.append(item)
                if w in 'Character Encoding':
                    for item in w3tech[w]:
                        character_encoding.append(item)
                if w in 'JavaScript Library':
                    for item in w3tech[w]:
                        js_frameworks.append(item)
                if w in 'Site Elements':
                    for item in w3tech[w]:
                        site_elements.append(item)
                if w in 'Web Server':
                    for item in w3tech[w]:
                        web_servers.append(item)
                if w in 'Traffic Analysis Tool':
                    for item in w3tech[w]:
                        analysis_tool.append(item)
                if w in 'Markup Language':
                    for item in w3tech[w]:
                        markup_lang.append(item)
                if w in 'Image File Formats':
                    for item in w3tech[w]:
                        img_formats.append(item)

            for bw in builtw:
                count = 0
                # print bw
                if bw in 'blogs':
                    for item in builtw[bw]:
                        blogs.append(item)
                if bw in 'mobile-frameworks':
                    for item in builtw[bw]:
                        mobile_frameworks.append(item)
                if bw in 'font-scripts':
                    for item in builtw[bw]:
                        font_scripts.append(item)
                if bw in 'web-servers':
                    for item in builtw[bw]:
                        web_servers.append(item)
                if bw in 'javascript-frameworks':
                    for item in builtw[bw]:
                        js_frameworks.append(item)
                if bw in 'programming-languages':
                    for item in builtw[bw]:
                        programming_lng.append(item)
                if bw in 'cms':
                    for item in builtw[bw]:
                        cms.append(item)
                if bw in 'ecommerce':
                    for item in builtw[bw]:
                        ecommerce.append(item)
                if bw in 'web-frameworks':
                    for item in builtw[bw]:
                        web_frameworks.append(item)
                if bw in 'operating-systems':
                    for item in builtw[bw]:
                        op_sys.append(item)
                if bw in 'cdn':
                    for item in builtw[bw]:
                        cdn.append(item)
                if bw in 'video-players':
                    for item in builtw[bw]:
                        video_players.append(item)

            # --------- get UNIQUE TECH ARRAYS --------- #
            blogs = compareData.CompareData.unique(blogs)
            mobile_frameworks = compareData.CompareData.unique(mobile_frameworks)
            font_scripts = compareData.CompareData.unique(font_scripts)
            web_servers = compareData.CompareData.unique(web_servers)
            js_frameworks = compareData.CompareData.unique(js_frameworks)
            programming_lng = compareData.CompareData.unique(programming_lng)
            cms = compareData.CompareData.unique(cms)
            ecommerce = compareData.CompareData.unique(ecommerce)
            web_frameworks = compareData.CompareData.unique(web_frameworks)
            op_sys = compareData.CompareData.unique(op_sys)
            cdn = compareData.CompareData.unique(cdn)
            video_players = compareData.CompareData.unique(video_players)
            character_encoding = compareData.CompareData.unique(character_encoding)
            site_elements = compareData.CompareData.unique(site_elements)
            analysis_tool = compareData.CompareData.unique(analysis_tool)
            markup_lang = compareData.CompareData.unique(markup_lang)
            img_formats = compareData.CompareData.unique(img_formats)

            # if entry with same date not in DB -> add to DB
            date_exists = compareData.CompareData.compare_dates(base_url, 'timestamp_tech')
            date = compareData.CompareData.get_date()

            if date_exists is False:
                mongo.setbuiltwith(blogs, mobile_frameworks, font_scripts,
                                   web_servers, js_frameworks, programming_lng,
                                   cms, ecommerce, web_frameworks, op_sys,
                                   cdn, video_players, character_encoding, site_elements,
                                   analysis_tool, markup_lang, img_formats, base_url, date)


            # mongo.print_db()

        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: builtwith_function " + " URL: " + url + ", " + "\n")
        finally:
            pass

    @staticmethod
    def fix_html(broken_html, url):
        """
        fix broken html
        :param broken_html:
        :param url:
        :return: fixed html
        """
        try:
            tree = lxml.html.fromstring(broken_html)
            fixed_html = lxml.html.tostring(tree, pretty_print=True)
            return fixed_html
        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: fix_html " + " URL: " + url + ", " + "\n")
        finally:
            pass

    @staticmethod
    def extract_data_by_css(html, sel, base_url):
        """
        extracting Data using CSS selectors
        :param html: html
        :param sel: selector, for example "title"
        :param base_url:
        :return: "Website Title"
        """
        try:
            tree = lxml.html.fromstring(html)
            selector = tree.cssselect(sel)[0]
            sel_content = selector.text_content()
            print sel_content
            return sel_content
        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: extract_data_by_css " + " URL: " + base_url + ", " + "\n")
        finally:
            pass

    @staticmethod
    def last_modified(url):
        """
        Get Header Data and Last Modified
        :param url: url of website
        :return: last_modified date if set
        """
        try:
            request = urllib2.Request(url)
            opener = urllib2.build_opener()
            header_data = opener.open(request)
            print "Header: ", header_data.headers.dict
            print "Last Modified: ", header_data.headers.get('Last-Modified')
        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: last_modified " + " URL: " + url + ", " + "\n")
        finally:
            pass

    @staticmethod
    def popularity_rank(url):
        """
        Get the popularity rank from alexa
        :param url:
        :return: alexa Popularity
        """
        try:
            soup = bs4.BeautifulSoup(urllib.urlopen('http://data.alexa.com/data?cli=10&dat=snbamz&url=' + url).read(),
                                     'xml')
            popularity = soup.find("POPULARITY")['TEXT']
            return popularity
        except exceptions.Exception as e:
            popularity = "None"
            logfile.write("!ERROR! FUNCTION: popularity_rank " + " URL: " + url + ", " + "\n")
            return popularity
        finally:
            pass

    @staticmethod
    def get_category(base_url):
        """
        get the category of the website
        :param base_url:
        :return: category array
        """
        try:
            url = 'http://sitereview.bluecoat.com/rest/categorization'

            useragent = {
                'User-Agent': 'Mozilla/5.0',
            }

            payload = {"url": base_url}
            print payload
            req = requests.post(
                url,
                headers=useragent,
                data=payload
            )
            response = json.loads(req.content)

            if req.status_code == 200:
                try:
                    category = bs4.BeautifulSoup(response["categorization"], "lxml").get_text()
                    categories = category.split("/")
                    return categories
                except:
                    pass


        except requests.ConnectionError:
            print "error"
            pass
