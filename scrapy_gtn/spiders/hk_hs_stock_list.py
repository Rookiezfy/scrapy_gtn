# -*- coding: utf-8 -*-
# scrapy crawl hk_stock -o hk_stock.csv
import sys
import os
# 临时修改环境变量 为当前目录上两级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(root_dir)
import scrapy
import json
from ..items import StockItem
import scrapy_gtn.conf.config as config
import logging as log

log.basicConfig(level=log.WARNING,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=root_dir + '/hk_stock.log', mode='a', encoding='utf-8'),
                          log.StreamHandler(sys.stderr)})

class HkHsStockSpider(scrapy.Spider):
    name = 'hk_hs_stock_list'

    def start_requests(self):
        start_url = 'http://52.push2.eastmoney.com/api/qt/clist/get/'
        headers = {
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Content-Type': 'application/javascript; charset=UTF-8'
        }
        # 700 100 150
        stock_type = [{'name':'港股','market':'hk','m_arg':'m:116','pages':700},
                      {'name':'沪深A股','market':'hs','m_arg':'m:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2','pages':200}]

        for stock_t in stock_type:
            pages = stock_t['pages']
            for page in range(1,pages):
                log.info('正在爬取第'+str(page)+'页'+stock_t['name']+'股票列表...')
                yield scrapy.FormRequest(callback=self.parse,dont_filter=True,url=start_url,method='GET',headers=headers,
                                     formdata={'pn': str(page), 'pz': '20', 'po': '1', 'np': '1','fltt':'2','invt':'2','fid':'f3', 'fs':stock_t['m_arg'],'fields':'f12,f13,f14'})


    def parse(self, response):
        response_str = str(response.text).replace("\n","").replace("\r","")
        data = json.loads(response_str)['data']
        if (data != None):
           res = data['diff']
           for one in res:
               item = StockItem()
               if (str(one['f13']) == '116'):#港股
                   item['secid'] = str(one['f13']) + '.' + str(one['f12'])
               elif(str(one['f13']) == '1'): #上证
                   item['secid'] = str(one['f12']+'1')
               elif (str(one['f13']) == '0'):  #深证
                   item['secid'] = str(one['f12'] + '2')
               else:
                   item['secid'] = str(one['f12'] + '_no')
               item['market'] = one['f13']
               item['stock_code'] = one['f12']
               item['stock_name'] = one['f14']
               yield item