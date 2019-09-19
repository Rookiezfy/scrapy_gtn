# -*- coding: utf-8 -*-
import sys
import os
# 临时修改环境变量 为当前目录上两级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(root_dir)
import scrapy
import pymysql
import logging as log
import scrapy_gtn.conf.config as config
import json
from ..items import QuotItem

log.basicConfig(level=log.WARNING,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=root_dir + '/hs_quotation_all.log', mode='a', encoding='utf-8'),
                          log.StreamHandler(sys.stderr)})
# 从东财爬取沪深A股行情-全量爬取，初始化时执行一次即可，后续使用增量爬虫
class HsQuotationAllSpider(scrapy.Spider):
    name = 'hs_quotation_all'

    def start_requests(self):
        start_url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js'
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Content-Type': 'text/json; charset=utf-8'
        }
        # 查询所有沪深A股股票列表
        connection = pymysql.connect(
            host=config.get_db_host(),
            db=config.get_db_dbname(),
            port=config.get_db_port(),
            user=config.get_db_username(),
            password=config.get_db_passwd(),
            charset=config.get_db_charset())
        cursor = connection.cursor()
        cursor.execute('select secid,market,stock_code,stock_name from hk_hs_stock_list where (market = "0" or market = "1") ')
        hs_stocks = cursor.fetchall()

        # k线频度及对应接口参数
        # m5k(5MIN) m15k(15MIN) m30k(30MIN)  m60k(60MIN) k(日) wk(周)  mk(月)
        freqs = ['m5k', 'm15k', 'm30k', 'm60k', 'k', 'wk', 'mk']

        for freq in freqs:
            for hs_stock in hs_stocks:
                log.info('正在爬取沪深A股[' + hs_stock[0] + hs_stock[3] + ']频度' + freq + '数据...')
                meta = {'secid': hs_stock[0],
                        'market': hs_stock[1],
                        'stock_code': hs_stock[2],
                        'stock_name': hs_stock[3],
                        'klt': freq}
                params = {'id': hs_stock[0],
                          'rtntype': '6',
                          'type': freq,
                          'authorityType': 'undefined'
                          }
                yield scrapy.FormRequest(callback=self.parse, dont_filter=True, url=start_url, method='GET',
                                         headers=headers,
                                         meta=meta, formdata=params)

    def parse(self, response):
        market = response.meta['market']
        stock_code = response.meta['stock_code']
        stock_name = response.meta['stock_name']
        secid = response.meta['secid']
        freq = response.meta['klt']

        text = str(response.text).replace("\n", "").replace("\r", "")
        response_str = text[1:len(text)-1]

        data = []
        try:
            data = json.loads(response_str)['data']
        except:
            log.error(secid + '爬取' + stock_code + stock_name + freq + '频度数据出错...')

        if (data != None and len(data) > 0):
            if (freq in ['wk', 'mk'] and len(data)>1):
                data.pop()  # 去除最后一天的数据，防止日k 周k出现多余数据
            for one in data:
                item = QuotItem()
                item['secid'] = secid
                item['market'] = market
                item['stock_code'] = stock_code
                item['stock_name'] = stock_name
                if (freq in ['m5k', 'm15k', 'm30k', 'm60k']): #分钟数据，处理交易时间字段
                    item['trade_time'] = str(one).split(',')[0]
                    item['trade_date'] = (str(one).split(',')[0])[0:10]
                else:
                    item['trade_time'] = ''
                    item['trade_date'] = str(one).split(',')[0]
                item['open_px'] = str(one).split(',')[1]
                item['high_px'] = str(one).split(',')[3]
                item['low_px'] = str(one).split(',')[4]
                item['close_px'] = str(one).split(',')[2]
                item['business_amount'] = str(one).split(',')[5]
                item['business_balance'] = str(one).split(',')[6]
                item['freq'] = freq
                yield item