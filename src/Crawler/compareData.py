from src.Configuration import mongocache
from decimal import *
import datetime
import collections

mongo = mongocache.MongoCache()



# compare Data from DB
class CompareData:

    def __init__(self):
        pass

    @staticmethod
    def get_items_css_array(item_comp, cap, timestamp, cat):
        """
        get css data array from db
        :param item_comp: item to get (for example colors)
        :param cap: capitalize or not
        :param timestamp: timestamp of entry
        :return:
        """
        try:
            items = []
            cursor = ''
            if cat == 'global':
                cursor = mongo.db.webpage.find({})
            if cat == 'AUT':
                cursor = mongo.db.webpage_aut.find({})
            if cat == 'design':
                cursor = mongo.db.webpage_design.find({})

            for key in cursor:
                if 'timestamp_css' in key:
                    for i, item in enumerate(key['timestamp_css']):
                        for k, value in item['css'].iteritems():
                            if item_comp == k:
                                if value is None:
                                    print "Value is None"
                                else:
                                    for v in value:
                                        v = v.replace("\\", '')
                                        if timestamp == item['time']:
                                            if cap:
                                                v = v.title()
                                            else:
                                                v = v.lower()
                                            if item_comp is 'fonts':
                                                if v == 'Inherit':
                                                    v = 'Inherit'
                                                else:
                                                    items.append(v)
                                            else:
                                                items.append(v)

            return items
        except:
            print "get_item_css_array FAILED"
            pass


    @staticmethod
    def get_items_tech_array(item_comp, cap, timestamp, cat):
        """
        get tech data array from db
        :param item_comp: item to get (for example web servers)
        :param cap: capitalize or not
        :param timestamp: timestamp of entry
        :return:
        """
        try:
            if cat == 'global':
                cursor = mongo.db.webpage.find({})
            if cat == 'AUT':
                cursor = mongo.db.webpage_aut.find({})
            if cat == 'design':
                cursor = mongo.db.webpage_design.find({})

            items = []

            for key in cursor:
                if 'timestamp_tech' in key:
                    for i, item in enumerate(key['timestamp_tech']):
                        try:
                            for k, value in item['technology'].iteritems():
                                for v in value:
                                    if timestamp == item['time']:
                                        if item_comp == k:
                                            items.append(v)
                        except:
                            print "FAILED"

            return items
        except:
            print "get_items_tech_array FAILED"
            pass

    @staticmethod
    def get_items_css(item_comp, cap, timestamp, cat):
        """
        get css data from db
        :param item_comp: item to get
        :param cap: capitalize or not
        :param timestamp: timestamp of entry
        :return:
        """
        try:
            if cat == 'global':
                cursor = mongo.db.webpage.find({})
            if cat == 'AUT':
                cursor = mongo.db.webpage_aut.find({})
            if cat == 'design':
                cursor = mongo.db.webpage_design.find({})

            items = []

            for key in cursor:
                if 'timestamp_css' in key:
                    for i, item in enumerate(key['timestamp_css']):
                        for k, value in item['css'].iteritems():
                            if timestamp == item['time']:
                                if item_comp == k:
                                    item_v = item['css'][k]
                                    if item_v:
                                        items.append(item_v)
            return items
        except:
            print "get_items_css FAILED"

    @staticmethod
    def get_items_tech(item_comp, cap, timestamp, cat):
        """
        get tech data from db
        :param item_comp: item to get
        :param cap: capitalize or not
        :param timestamp: timestamp of entry
        :return:
        """
        try:
            if cat == 'global':
                cursor = mongo.db.webpage.find({})
            if cat == 'AUT':
                cursor = mongo.db.webpage_aut.find({})
            if cat == 'design':
                cursor = mongo.db.webpage_design.find({})

            items = []

            for key in cursor:
                if 'timestamp_tech' in key:
                    for i, item in enumerate(key['timestamp_tech']):
                        for k, value in item['technology'].iteritems():
                            if timestamp == item['time']:
                                if item_comp == k:
                                    item_v = item['technology'][k]
                                    if item_v:
                                        items.append(item_v)
            return items
        except:
            print "get_items_tech FAILED"


    @staticmethod
    def compare_data(items):
        """
        get 100 most common items
        :param items: for example colors
        :return: most common 100 items
        """

        try:
            counter = collections.Counter(items)
            return counter.most_common(500)
        except:
            print "compare Data failed"

    @staticmethod
    def get_mapping(items):
        arr = []
        counter = 0

        for i in items:
            arr.append([])
            arr[counter].append(i[0].encode("utf-8"))
            arr[counter].append(i[1])
            counter += 1

        return arr

    @staticmethod
    def get_percentage(items, itemsRaw):
        """
        get percentages of items
        :param items: compared items
        :param itemsRaw: items uncompared
        :return: percentage list
        """
        try:
            countAll = len(itemsRaw)
            index = 0
            percentageItems = []
            percentageItems.append([])
            lst = list(items)
            percentageList = list()

            for item in lst:
                count = item[1]
                item = list(item)
                percentage = Decimal(item[1])/Decimal(countAll) * Decimal(100)
                fontSize = percentage*20
                width = percentage * 100
                width = round(width, -1)
                fontSize = round(fontSize, -1)
                percentage = "%.2f" % percentage
                item[1] = percentage
                item.append(fontSize)
                item.append(count)
                percentageList.append(item)
                item.append(width)
                index += 1

            return percentageList
        except:
            print "failed"
        finally:
            pass

    @staticmethod
    def get_date():
        """
        get current date in the correct format
        :return: current date
        """
        date = datetime.datetime.now().date()
        date = str(date)
        date = date.replace('datetime.date(', '')
        date = date.replace(')', '')
        date = '2017-01-25';
        return date

    @staticmethod
    def get_date_from_db(base_url, timestamp):
        """
        get timestamp of entry from db
        :param base_url: entry to compare
        :param timestamp: timestamp of entry
        :return: timestamps
        """
        dates = []
        try:
            basic = mongo.db.webpage.find_one({'_id': base_url})
            dates = []

            for i, item in enumerate(basic[timestamp]):
                dates.append(basic[timestamp][i]['time'])

            return dates
        except:
            print "get_date_from_db FAILED"
            return dates

    @staticmethod
    def get_timestamps():
        """
        get all timestamps
        :return: timestamps
        """
        dates = []
        try:
            basic = mongo.db.webpage.find({})
            dates = []
            for key in basic:
                if 'timestamp_tech' in key:
                    for i, item in enumerate(key['timestamp_tech']):
                        for k, value in item['technology'].iteritems():
                            item_v = item['time']
                            dates.append(item_v)
            return dates
        except:
            print "get_date_from_db FAILED"
            return dates

    @staticmethod
    def combine_lists(list1, list2):
        merged_list = list1 + list2
        return merged_list

    @staticmethod
    def compare_dates(base_url, timestamp):
        """
        compare current date with timestamps
        :param base_url:
        :param timestamp:
        :return: false, true
        """
        try:
            date = CompareData.get_date()
            dates = CompareData.get_date_from_db(base_url, timestamp)
            if dates == []:
                return False
            for d in dates:
                if str(d) == date:
                    return True

            return False
        except:
            print "compare_dates FAILED"
            return False

    @staticmethod
    def get_nr_of_websites():
        cursor = mongo.db.webpage.find({})
        count = 0
        for key in cursor:
            if 'timestamp_css' in key:
                count += 1


        #websites = cursor.count()
        return count

    @staticmethod
    def unique(seq):
        """
        get unique entries in an array
        :param seq:
        :return: unique array
        """
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    @staticmethod
    def color_not_neutral(items):
        with open('neutral_colors.txt') as f:
            content = f.readlines()

        content = [x.strip() for x in content]

        colorful = []
        for i in items:
            i = i.upper()
            if i in content:
                print i
            else:
                colorful.append(i)

        return colorful