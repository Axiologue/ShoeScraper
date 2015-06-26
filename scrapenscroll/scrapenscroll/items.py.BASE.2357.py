# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    division = scrapy.Field()
    category = scrapy.Field()
    image_link = scrapy.Field()
    price = scrapy.Field()
