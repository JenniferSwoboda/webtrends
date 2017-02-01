

class Printer:
    def __init__(self):
        pass

    @staticmethod
    def print_list(list):
        try:
            for item in list:
                print item
        except:
            pass

    @staticmethod
    def prettifyOutput(title):
        print '---------------' + title + "---------------"
