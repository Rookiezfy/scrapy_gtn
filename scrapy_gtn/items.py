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

# 沪深A股、港股股票信息
class StockItem(scrapy.Item):
    secid = Field() # 股票代码
    market = Field() # 市场代码
    stock_code = Field() # 股票代码
    stock_name = Field() # 股票名称

# 美股股票信息
class USStockItem(scrapy.Item):
    symbol = Field() # 股票代码
    market = Field() # 市场
    stock_name = Field() # 股票名称

# 港股、沪深A股行情
class QuotItem(scrapy.Item):
    secid = Field()  # 用于从接口查询的代码，市场代码.股票代码
    market = Field()  # 市场代码
    stock_code = Field() #股票代码
    stock_name = Field() #股票名称
    trade_date = Field()  #交易日期
    trade_time = Field() #交易时间
    open_px = Field()  #开盘价
    high_px = Field()  #最高价
    low_px = Field()  #最低价
    close_px = Field()  #收盘价
    business_amount = Field()  #成交量
    business_balance = Field()  #成交额(元)
    freq = Field()  #频度

