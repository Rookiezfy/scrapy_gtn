# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ScrapyGtnItem(scrapy.Item):
    website = Field()
    url = Field()
    title = Field()
    abstract = Field()
    content = Field()
    datetime = Field()
    original = Field()
    author = Field()

# 港股股票信息
class StockItem(scrapy.Item):
    secid = Field() # 股票代码 市场代码+编号 116.19457
    market = Field() # 市场代码
    stock_code = Field() # 股票代码 港股116
    stock_name = Field() # 股票名称

# 港股行情
class HkQuotItem(scrapy.Item):
    stock_code = Field() #股票代码
    trade_date = Field()  #交易日期
    open_px = Field()  #开盘价
    high_px = Field()  #最高价
    low_px = Field()  #最低价
    close_px = Field()  #收盘价
    business_amount = Field()  #成交量
    business_balance = Field()  #成交额(元)
    freq = Field()  #频度
    secid =Field() #用于从接口查询的代码，市场代码.股票代码
    market = Field() #市场代码
