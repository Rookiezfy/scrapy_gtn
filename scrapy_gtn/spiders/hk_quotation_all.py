# -*- coding: utf-8 -*-
# scrapy crawl hk_quotation -o hk_quotation.csv
import sys
import os
# 临时修改环境变量 为当前目录上两级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(root_dir)
import scrapy
import json
from ..items import QuotItem
import scrapy_gtn.conf.config as config
import logging as log
import pymysql
import datetime
from dateutil.relativedelta import relativedelta

log.basicConfig(level=log.WARNING,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=root_dir + '/hk_quotation_all.log', mode='a', encoding='utf-8'),
                          log.StreamHandler(sys.stderr)})
# 从东财爬取港股行情
class HkQuotationAllSpider(scrapy.Spider):
    name = 'hk_quotation_all'

    def start_requests(self):
        start_url = 'http://69.push2his.eastmoney.com/api/qt/stock/kline/get'
        headers = {
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Content-Type': 'application/javascript; charset=UTF-8'
        }

        # 查询所有港股股票列表
        connection = pymysql.connect(
            host=config.get_db_host(),
            db=config.get_db_dbname(),
            port=config.get_db_port(),
            user=config.get_db_username(),
            password=config.get_db_passwd(),
            charset=config.get_db_charset())
        cursor = connection.cursor()
        cursor.execute('select secid,market,stock_code,stock_name from hk_hs_stock_list where market = "116" limit 1')
        hk_stocks = cursor.fetchall()

        # k线频度 日 周 月
        freqs = ['101','102','103']

        end_date = datetime.datetime.now().date().strftime('%Y%m%d')

        for freq in freqs:
            for hk_stock in hk_stocks:
                log.info('正在爬取港股['+hk_stock[0]+hk_stock[3]+']频度'+freq+'k线数据...')
                meta = {'secid':hk_stock[0],
                        'market':hk_stock[1],
                        'stock_code': hk_stock[2],
                        'stock_name': hk_stock[3],
                        'klt': freq}
                params = {'secid':hk_stock[0],
                          'fields1':'f1,f2,f3,f4,f5',
                          'fields2':'f51,f52,f53,f54,f55,f56,f57',
                          'klt': freq,
                          'fqt':'0',
                          'beg':'00000000',
                          'end':end_date}
                yield scrapy.FormRequest(callback=self.parse,dont_filter=True,url=start_url,method='GET',headers=headers,
                                     meta=meta,formdata=params)

    def parse(self, response):
        response_str = str(response.text).replace("\n","").replace("\r","")
        data = json.loads(response_str)['data']
        if (data != None):
           res = data['klines']
           market = response.meta['market']
           stock_code = response.meta['stock_code']
           stock_name = response.meta['stock_name']
           secid = response.meta['secid']
           freq = response.meta['klt']

           if (freq != '101' and len(res)>0): #周线和月线 去除最后条数据 防止周k 月k出现多余数据
               res.pop()

           for one in res:
               item = QuotItem()
               item['secid'] = secid
               item['market'] = market
               item['stock_code'] = stock_code
               item['stock_name'] = stock_name
               item['trade_date'] = str(one).split(',')[0]
               item['open_px'] = str(one).split(',')[1]
               item['high_px'] = str(one).split(',')[3]
               item['low_px'] = str(one).split(',')[4]
               item['close_px'] = str(one).split(',')[2]
               item['business_amount'] = str(one).split(',')[5]
               item['business_balance'] = str(one).split(',')[6]
               item['freq'] = freq
               yield item