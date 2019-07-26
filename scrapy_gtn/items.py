# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ScrapyGtnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website = Field()
    url = Field()
    title = Field()
    abstract = Field()
    content = Field()
    datetime = Field()
    original = Field()
    author = Field()
