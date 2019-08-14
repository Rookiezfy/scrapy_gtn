# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import os
import sys
# 临时修改环境变量 为当前目录上级目录
root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(root_dir)
from twisted.enterprise import adbapi
import scrapy_gtn.conf.config as config
import logging as log
import scrapy_gtn.items as items
import datetime
import decimal

# 异步机制将数据写入到mysql数据库中
class HkStockPipeline(object):
    def __init__(self):
        dbparms = dict(
            host=config.get_db_host(),
            db=config.get_db_dbname(),
            port=config.get_db_port(),
            user=config.get_db_username(),
            password=config.get_db_passwd(),
            charset=config.get_db_charset(),
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparms)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
    def do_insert(self,cursor,item):
        # 沪深 港股股票列表
        if isinstance(item, items.StockItem):
            sql = 'insert into hk_hs_stock_list(secid,market,stock_code,stock_name) VALUES (%s,%s,%s,%s) on duplicate key update market = %s,stock_code = %s, stock_name = %s'
            lis = (item['secid'], item['market'], item['stock_code'], item['stock_name'],item['market'], item['stock_code'], item['stock_name'])
            cursor.execute(sql, lis)

        # 美股股票列表
        if isinstance(item, items.USStockItem):
            sql = 'insert into us_stock_list(symbol,market,stock_name) VALUES (%s,%s,%s) on duplicate key update market = %s, stock_name = %s'
            lis = (item['symbol'], item['market'], item['stock_name'],item['market'], item['stock_name'])
            cursor.execute(sql, lis)

        # 港股行情
        if isinstance(item, items.QuotItem):
            table_name = ''
            min_k = False
            # 日k
            if(item['freq'] == '101' or item['freq'] == 'k'):
                table_name = 'rt_stock_daily'
            # 周k
            if(item['freq'] == '102' or item['freq'] == 'wk'):
                table_name = 'rt_stock_weekly'
            # 月k
            if(item['freq'] == '103' or item['freq'] == 'mk'):
                table_name = 'rt_stock_monthly'
            # 5分钟k
            if(item['freq'] == 'm5k'):
                table_name = 'rt_stock_5min'
                min_k = True
            # 15分钟k
            if (item['freq'] == 'm15k'):
                table_name = 'rt_stock_15min'
                min_k = True
            # 30分钟k
            if (item['freq'] == 'm30k'):
                table_name = 'rt_stock_30min'
                min_k = True
            # 60分钟k
            if (item['freq'] == 'm60k'):
                table_name = 'rt_stock_60min'
                min_k = True

            # 处理东财返回成交量、成交额 数据中以文字表示的数值，包括 万 亿，统一成个位数
            business_amount = ''
            if (str(item['business_amount']).find('万') >= 0 ):
                business_amount = decimal.Decimal(str(item['business_amount']).replace('万','')) * 10000
            elif (str(item['business_amount']).find('亿') >= 0 ):
                business_amount = decimal.Decimal(str(item['business_amount']).replace('亿', '')) * 100000000
            else:
                business_amount = item['business_amount']

            business_balance = ''
            if (str(item['business_balance']).find('万') >= 0 ):
                business_balance = decimal.Decimal(str(item['business_balance']).replace('万','')) * 10000
            elif (str(item['business_balance']).find('亿') >= 0 ):
                business_balance = decimal.Decimal(str(item['business_balance']).replace('亿', '')) * 100000000
            else:
                business_balance = item['business_balance']

            sql = ''
            lis = ()

            # 非分钟数据不包括trade_time字段
            if (min_k == False):
                sql = 'insert into ' + table_name + '(secid,market,stock_code,stock_name,trade_date,open_px,high_px,low_px,close_px,business_amount,business_balance) ' \
                                                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ' \
                                                'on duplicate key update market = %s,stock_code = %s,stock_name = %s,open_px = %s,high_px = %s,low_px = %s,close_px = %s,business_amount = %s,business_balance = %s,last_upd_time = %s'

                lis = (item['secid'], item['market'], item['stock_code'], item['stock_name'], item['trade_date'],
                       item['open_px'], item['high_px'], item['low_px'], item['close_px'],
                       business_amount, business_balance,
                       item['market'], item['stock_code'], item['stock_name'], item['open_px'], item['high_px'],
                       item['low_px'], item['close_px'],
                       business_amount, business_balance, datetime.datetime.now())

            else:
                sql = 'insert into ' + table_name + '(secid,market,stock_code,stock_name,trade_date,trade_time,open_px,high_px,low_px,close_px,business_amount,business_balance) ' \
                                                    'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ' \
                                                    'on duplicate key update market = %s,stock_code = %s,stock_name = %s,open_px = %s,high_px = %s,low_px = %s,close_px = %s,business_amount = %s,business_balance = %s,last_upd_time = %s'

                lis = (item['secid'], item['market'], item['stock_code'], item['stock_name'], item['trade_date'],item['trade_time'],
                       item['open_px'], item['high_px'], item['low_px'], item['close_px'],
                       business_amount, business_balance,
                       item['market'], item['stock_code'], item['stock_name'], item['open_px'], item['high_px'],
                       item['low_px'], item['close_px'],
                       business_amount, business_balance, datetime.datetime.now())

            cursor.execute(sql, lis)

    def handle_error(self, failure):
        log.error(failure)