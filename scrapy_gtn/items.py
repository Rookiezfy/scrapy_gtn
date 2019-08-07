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

# 港股股票信息
class HkStockItem(scrapy.Item):
    secid = Field() # 股票代码 市场代码+编号 116.19457
    code = Field() #代码
    name = Field() #名称
    market = Field() #市场代码
