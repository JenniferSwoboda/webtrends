import logging
import urllib
import bs4
import cssutils
import crawler
from src.Configuration import printer, converter, mongocache, download
from src.Crawler import compareData
import exceptions
import requests

logfile = open('errors_cssCrawler', 'w')
mongo = mongocache.MongoCache()

class CssCrawler:
    def __init__(self):
        pass

    @staticmethod
    def craw_css_data(url):
        """
        Crawl the css data of a website and save it in mongo DB
        :param url: website url
        :return:
        """

        # --------- Get Base URL --------- #
        base_url = crawler.Crawler.get_base_URL(url)
        url = 'http://' + base_url

        # --------- Download HTML --------- #
        D = download.Downloader()
        html = D(url)

        # --------- GET FONTS OF WEBSITE --------- #
        printer.Printer.prettifyOutput("FONTS")
        stylesheets = CssCrawler.crawl_stylesheets(url, html)
        print "Stylesheet"
        try:
            fonts = CssCrawler.crawl_css_prop(url, stylesheets, 'font-family')
            fonts = converter.Converter.convert_fonts(fonts)
        except:
            fonts = []
            pass
        #printer.Printer.print_list(fonts)

        # --------- GET COLORS OF WEBSITE --------- #
        printer.Printer.prettifyOutput("COLORS")
        try:
            colors = CssCrawler.crawl_css_prop(url, stylesheets, 'color')
            colors = converter.Converter.convert_to_hex(colors)
        except:
            colors = []
            pass
        # printer.Printer.print_list(colors)

        # --------- GET BG-COLORS OF WEBSITE --------- #
        try:
            background_colors = CssCrawler.crawl_css_prop(url, stylesheets, 'background-color')
            background_colors = converter.Converter.convert_to_hex(background_colors)
        except:
            background_colors = []
            pass

        # --------- MOBILE OR ADAPTIVE WEBSITE --------- #
        printer.Printer.prettifyOutput("MOBILE")
        responsive = CssCrawler.is_responsive(url)
        print responsive
        print "---------"

        date_exists = compareData.CompareData.compare_dates(base_url, 'timestamp_css')
        print date_exists
        date = compareData.CompareData.get_date()

        # --------- SAVE INTO MONGO DB --------- #
        if date_exists is False:
            mongo.setcss(fonts, colors, background_colors, responsive, base_url, date)

       # mongo.print_db()

    # Get all Stylesheets of the page
    @staticmethod
    def crawl_stylesheets(url, html):
        """
        crawl stylesheets of website
        :param url: url of website
        :param html: html of website
        :return: stylesheets list
        """
        try:
            # styleseets
            base_url = crawler.Crawler.get_base_URL(url)
            soup = bs4.BeautifulSoup(html, "lxml")
            links = soup.findAll("link", attrs={"rel": "stylesheet"})
            link_list = []
            for link in links:
                link_href = link.get('href')
                if not link_href.startswith('/') and not link_href.startswith('http'):
                    link_href = "/" + link_href
                if base_url in link_href:
                    link_list.append(link_href)
                elif not link_href.startswith('//') and not link_href.startswith('http'):
                    link_href = url + link_href

                    link_list.append(link_href)
                elif link_href.startswith('//'):
                    link_href = link_href.replace('//', 'http://')
                    link_list.append(link_href)
                else:
                    link_list.append(link_href)


            if not link_list:
                print "No Stylesheets found: " + url
                logfile.write("!ERROR(empty)! FUNCTION: crawl_stylesheets " + " URL: " + url + ", " + "\n")

            return link_list

        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: crawl_stylesheets " + " URL: " + url + ", " + "\n")
        finally:
            pass


    # Crawl for css properties
    @staticmethod
    def crawl_css_prop(url, links, prop):
        """
        crawl for a css property, for example "font-family"
        :param url: url of website to crawl
        :param links: stylesheet links
        :param prop: property to crawl for (color, font-family)
        :return: list of property values
        """
        try:
            # stylesheets
            cssutils.log.setLevel(logging.CRITICAL)
            prop_list = []
            links.append(url)
            sheet = ""
            for link in links:
                # inline styles
                if link is url:
                    html = urllib.urlopen(url).read()
                    html = unicode(html, errors='replace')
                    soup = bs4.BeautifulSoup(html, 'lxml')
                    styles = soup.findAll("style")
                    for style in styles:
                        style = str(style)
                        style = style.replace('</style>', '')
                        style = style.replace('<style>', '')
                        style = style.replace('<style type="text/css">', '')
                        sheet = cssutils.parseString(style)
                # stylesheets
                else:
                    link = link.replace('../', '')
                    soup = urllib.urlopen(link)
                    soup = soup.read()
                    soup = unicode(soup, errors='replace')
                    sheet = cssutils.parseString(soup)

                for rule in sheet:
                    # font-face
                    if prop == 'font-family':
                        if rule.type == rule.FONT_FACE_RULE:
                            for p in rule.style:
                                if p.name == prop:
                                    prop_list.append(p.value)

                    if rule.type == rule.STYLE_RULE:
                        for p in rule.style:
                            if p.name == prop:
                                prop_list.append(p.value)

            property_list = list(set(prop_list))

            if not property_list:
                print "No Item found: " + prop
                logfile.write("!ERROR(empty)! FUNCTION: crawl_css_prop " + " no item found: " + prop + ", " + "\n")

            return property_list

        except exceptions.Exception as e:
            print e
            logfile.write("!ERROR! FUNCTION: crawl_css_prop " + " link: " + links + ", " + "\n")
        finally:
            pass

    @staticmethod
    def is_responsive(url):
        """
        check if the website is responsive, adaptive or not responsive
        :param url: url of the website
        :return: adaptive, responsive or False
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
            }
            response = requests.get(url, headers=headers)
            mobile_url = response.url
            mobile_base_url = crawler.Crawler.get_base_URL(mobile_url)
            print mobile_url
            if response.status_code == 200 and mobile_base_url.startswith('mobile.') or mobile_base_url.startswith('mobil.') or mobile_base_url.startswith('m.'):
                print mobile_url
                return "adaptive"
            else:
                html = urllib.urlopen(url).read()
                html = unicode(html, errors='replace')

                soup = bs4.BeautifulSoup(html, "lxml")
                meta_tags = soup.findAll("meta", attrs={"name": "viewport"})
                for meta_tag in meta_tags:
                    meta_tag = str(meta_tag)
                    if "width=device-width" in meta_tag or "width = device-width" in meta_tag:
                            return "responsive"
                    else:
                        print "website not responsive"
                        return False
            return False

        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: is_responsive " + " URL: " + url + ", " + "\n")
        finally:
            pass
