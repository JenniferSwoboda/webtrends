from flask import Flask, render_template
from src.Crawler import compareData
from src.Configuration import mongocache

mongo = mongocache.MongoCache()
app = Flask(__name__)
c = compareData.CompareData

# Enter Timestamp to display
timestamp = '2017-01-25'
timestamps = c.unique(c.get_timestamps())
website_nrs = c.get_nr_of_websites()



# ALEXA GLOBAL TOP 100
cat = 'global'
percentageColors = c.get_percentage(c.compare_data(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat))), c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat)))
percentageColorful = c.get_percentage(c.compare_data(c.color_not_neutral(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat)))), c.color_not_neutral(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat))))
percentageFonts = c.get_percentage(c.compare_data(c.get_items_css_array('fonts', True, timestamp, cat)), c.get_items_css_array('fonts', True, timestamp, cat))
mapping_resp = c.get_mapping(c.compare_data(c.get_items_css('responsive', False, timestamp, cat)))
mapping_webserver = c.get_mapping(c.compare_data(c.get_items_tech_array('web_servers', False, timestamp, cat)))
mapping_js_frameworks = c.get_mapping(c.compare_data(c.get_items_tech_array('js_frameworks', False, timestamp, cat)))
mapping_programming_lang = c.get_mapping(c.compare_data(c.get_items_tech_array('programming_lng', False, timestamp, cat)))
mapping_markup_lang = c.get_mapping(c.compare_data(c.get_items_tech_array('markup_lang', False, timestamp, cat)))
mapping_site_elem = c.get_mapping(c.compare_data(c.get_items_tech_array('site_elements', False, timestamp, cat)))
mapping_font_scripts= c.get_mapping(c.compare_data(c.get_items_tech_array('font_scripts', False, timestamp, cat)))
mapping_encodings= c.get_mapping(c.compare_data(c.get_items_tech_array('character_encoding', False, timestamp, cat)))
mapping_img_formats= c.get_mapping(c.compare_data(c.get_items_tech_array('img_formats', False, timestamp, cat)))
mapping_analysis_tool = c.get_mapping(c.compare_data(c.get_items_tech_array('analysis_tool', False, timestamp, cat)))


# ALEXA AUSTRIA TOP 100
cat = 'AUT'
at_percentageColors = c.get_percentage(c.compare_data(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat))), c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat)))
at_percentageColorful = c.get_percentage(c.compare_data(c.color_not_neutral(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat)))), c.color_not_neutral(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat))))
at_percentageFonts = c.get_percentage(c.compare_data(c.get_items_css_array('fonts', True, timestamp, cat)), c.get_items_css_array('fonts', True, timestamp, cat))
at_mapping_resp = c.get_mapping(c.compare_data(c.get_items_css('responsive', False, timestamp, cat)))
at_mapping_webserver = c.get_mapping(c.compare_data(c.get_items_tech_array('web_servers', False, timestamp, cat)))
at_mapping_js_frameworks = c.get_mapping(c.compare_data(c.get_items_tech_array('js_frameworks', False, timestamp, cat)))
at_mapping_programming_lang = c.get_mapping(c.compare_data(c.get_items_tech_array('programming_lng', False, timestamp, cat)))
at_mapping_markup_lang = c.get_mapping(c.compare_data(c.get_items_tech_array('markup_lang', False, timestamp, cat)))
at_mapping_site_elem = c.get_mapping(c.compare_data(c.get_items_tech_array('site_elements', False, timestamp, cat)))
at_mapping_font_scripts= c.get_mapping(c.compare_data(c.get_items_tech_array('font_scripts', False, timestamp, cat)))
at_mapping_encodings= c.get_mapping(c.compare_data(c.get_items_tech_array('character_encoding', False, timestamp, cat)))
at_mapping_img_formats= c.get_mapping(c.compare_data(c.get_items_tech_array('img_formats', False, timestamp, cat)))
at_mapping_analysis_tool = c.get_mapping(c.compare_data(c.get_items_tech_array('analysis_tool', False, timestamp, cat)))


# ALEXA DESIGN TOP 100
cat = 'design'
design_percentageColors = c.get_percentage(c.compare_data(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat))), c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat)))
design_percentageColorful = c.get_percentage(c.compare_data(c.color_not_neutral(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat)))), c.color_not_neutral(c.combine_lists(c.get_items_css_array('colors', False, timestamp, cat),c.get_items_css_array('bg_colors', False, timestamp, cat))))
design_percentageFonts = c.get_percentage(c.compare_data(c.get_items_css_array('fonts', True, timestamp, cat)), c.get_items_css_array('fonts', True, timestamp, cat))
design_mapping_resp = c.get_mapping(c.compare_data(c.get_items_css('responsive', False, timestamp, cat)))
design_mapping_webserver = c.get_mapping(c.compare_data(c.get_items_tech_array('web_servers', False, timestamp, cat)))
design_mapping_js_frameworks = c.get_mapping(c.compare_data(c.get_items_tech_array('js_frameworks', False, timestamp, cat)))
design_mapping_programming_lang = c.get_mapping(c.compare_data(c.get_items_tech_array('programming_lng', False, timestamp, cat)))
design_mapping_markup_lang = c.get_mapping(c.compare_data(c.get_items_tech_array('markup_lang', False, timestamp, cat)))
design_mapping_site_elem = c.get_mapping(c.compare_data(c.get_items_tech_array('site_elements', False, timestamp, cat)))
design_mapping_font_scripts= c.get_mapping(c.compare_data(c.get_items_tech_array('font_scripts', False, timestamp, cat)))
design_mapping_encodings= c.get_mapping(c.compare_data(c.get_items_tech_array('character_encoding', False, timestamp, cat)))
design_mapping_img_formats= c.get_mapping(c.compare_data(c.get_items_tech_array('img_formats', False, timestamp, cat)))
design_mapping_analysis_tool = c.get_mapping(c.compare_data(c.get_items_tech_array('analysis_tool', False, timestamp, cat)))

@app.route('/')
def index(fonts=percentageFonts, colors=percentageColors, responsive=mapping_resp,
                programming_lng=mapping_programming_lang,
                js_frameworks=mapping_js_frameworks, web_servers=mapping_webserver,
                font_scripts=mapping_font_scripts,
                encoding=mapping_encodings, site_elem=mapping_site_elem,
                analysis_tool=mapping_analysis_tool, markup_lang=mapping_markup_lang, img_formats=mapping_img_formats, colorful=percentageColorful,
                url_title='Top 100 Alex Websites GLOBAL'):
    return render_template('index.html', fonts=fonts, colors=colors, responsive=responsive,
                           programming_lng=programming_lng,
                           js_frameworks=js_frameworks, web_servers=web_servers,
                           font_scripts=font_scripts, encoding=encoding, site_elem=site_elem,
                           analysis_tool=analysis_tool, markup_lang=markup_lang, img_formats=img_formats,
                           colorful=colorful, url_title=url_title)


@app.route('/AT')
def index_at(fonts=at_percentageFonts, colors=at_percentageColors, responsive=at_mapping_resp,
                programming_lng=at_mapping_programming_lang,
                js_frameworks=at_mapping_js_frameworks, web_servers=at_mapping_webserver,
                font_scripts=at_mapping_font_scripts,
                encoding=at_mapping_encodings, site_elem=at_mapping_site_elem,
                analysis_tool=at_mapping_analysis_tool, markup_lang=at_mapping_markup_lang, img_formats=at_mapping_img_formats,
                colorful=at_percentageColorful,
                url_title='Top 100 Alex Websites AUSTRIA'):
    return render_template('index.html', fonts=fonts, colors=colors, responsive=responsive,
                           programming_lng=programming_lng,
                           js_frameworks=js_frameworks, web_servers=web_servers,
                           font_scripts=font_scripts, encoding=encoding, site_elem=site_elem,
                           analysis_tool=analysis_tool, markup_lang=markup_lang, img_formats=img_formats,
                           colorful=colorful, url_title=url_title)



@app.route('/design')
def index_design(fonts=design_percentageFonts, colors=design_percentageColors, responsive=design_mapping_resp,
                programming_lng=design_mapping_programming_lang,
                js_frameworks=design_mapping_js_frameworks, web_servers=design_mapping_webserver,
                font_scripts=design_mapping_font_scripts,
                encoding=design_mapping_encodings, site_elem=design_mapping_site_elem,
                analysis_tool=design_mapping_analysis_tool, markup_lang=design_mapping_markup_lang, img_formats=design_mapping_img_formats,
                colorful=design_percentageColorful,
                url_title='Top 100 Alex Websites DESIGN'):
    return render_template('index.html', fonts=fonts, colors=colors, responsive=responsive,
                           programming_lng=programming_lng,
                           js_frameworks=js_frameworks, web_servers=web_servers,
                           font_scripts=font_scripts, encoding=encoding, site_elem=site_elem,
                           analysis_tool=analysis_tool, markup_lang=markup_lang, img_formats=img_formats,
                           colorful=colorful, url_title=url_title)


if __name__ == "__main__":
    app.run()

