import tushare as ts
from scrapy_gtn.conf import config
# 沪深股票列表 写入stock_basic.csv

# 获取沪深A股股票信息 https://tushare.pro/document/2?doc_id=25 并写入stock_basic.csv
def get_stock_basic():
    ts.set_token(config.get_token())
    stock = ts.pro_api().query('stock_basic', exchange='', list_status='', fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    stock.to_csv(config.get_data_dir() + 'stock_basic.csv', index=False, sep=',')
    return config.get_data_dir() + 'stock_basic.csv'
