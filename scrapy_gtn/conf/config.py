class GlobalVar:
    # ts token
    ts_token = '87ca2f52711feb88ff84df57ad8f350662499b563bd9f48e917bc5e2'

    # 结果文件存放路径 相对于根路径E:/01git/python/scrapy_gtn/
    data_dir = '/scrapy_gtn/data/'

    # 日志文件格式
    log_format = '[%(levelname)s]%(asctime)s %(name)s: %(message)s'

    # 日志时间格式
    log_datefmt = '%Y-%m-%d %H:%M:%S'

    # 数据库配置
    db_host = '127.0.0.1'

    db_port = 3306

    db_username = 'root'

    db_passwd = '123456'

    db_dbname = 'tushare'

    db_charset = 'utf8'

def get_token():
    return GlobalVar.ts_token
def get_data_dir():
    return GlobalVar.data_dir
def get_log_format():
    return GlobalVar.log_format
def get_log_datefmt():
    return GlobalVar.log_datefmt
def get_db_host():
    return GlobalVar.db_host
def get_db_port():
    return GlobalVar.db_port
def get_db_username():
    return GlobalVar.db_username
def get_db_passwd():
    return GlobalVar.db_passwd
def get_db_dbname():
    return GlobalVar.db_dbname
def get_db_charset():
    return GlobalVar.db_charset


