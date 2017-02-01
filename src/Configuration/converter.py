import webcolors
import exceptions


logfile = open('errors_converter', 'w')

class Converter:
    def __init__(self):
        pass


    @staticmethod
    def convert_to_hex(colors):
        try:
            hex_list = []

            for color in colors:
                if not color.startswith('inherit') and not color.startswith('transparent'):
                    if color.startswith('rgba'):
                        color = color.replace('rgba', '').replace('(', '').replace(')', '').replace(' ', '')
                        c = color.split(',')
                        r = int(c[0])
                        g = int(c[1])
                        b = int(c[2])
                        a = float(c[3])
                        color = webcolors.rgb_to_hex((r, g, b, a))
                        print color
                    elif color.startswith('rgb'):
                        color = color.replace('rgb', '').replace('(', '').replace(')', '').replace(' ', '')
                        c = color.split(',')
                        r = int(c[0])
                        g = int(c[1])
                        b = int(c[2])
                        color = webcolors.rgb_to_hex((r, g, b))
                        print color
                    elif color.startswith('#'):
                        color = webcolors.normalize_hex(color)
                        print color
                    else:
                        try:
                            color = webcolors.name_to_hex(color)
                        except:
                            pass
                    hex_list.append(color)
                    hex_list = list(set(hex_list))
            return hex_list

        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: convert_to_hex " + "\n")
        finally:
            pass


    @staticmethod
    def convert_fonts(fonts):
        try:
            font_list = []
            print "FONTS"
            for font in fonts:
                font = font.lower()
                font = font.replace('"', '')
                if "," in font:
                    y = font.split(",")
                    # only first font of font-family
                    font_list.append(y[0])
                else:
                    font_list.append(font)
            fonts_list = list(set(font_list))
            return fonts_list
        except exceptions.Exception as e:
            logfile.write("!ERROR! FUNCTION: convert_fonts " + " URL: " + fonts + ", " + "\n")
        finally:
            pass
