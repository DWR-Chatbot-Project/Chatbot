# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Regulation(scrapy.Item):
    # define the fields for your item here like:
    # rule_url = scrapy.Field()
    chapter = scrapy.Field()
    article = scrapy.Field()
    title = scrapy.Field()
    paragraphText = scrapy.Field()
