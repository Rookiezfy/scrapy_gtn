class GlobalVar:
    # ts token
    ts_token = '87ca2f52711feb88ff84df57ad8f350662499b563bd9f48e917bc5e2'

    # 结果文件存放路径 相对于根路径E:/01git/python/scrapy_gtn/
    data_dir = '/scrapy_gtn/data/'

    # 日志文件格式
    log_format = '[%(levelname)s]%(asctime)s %(name)s: %(message)s'

    # 日志时间格式
    log_datefmt = '%Y-%m-%d %H:%M:%S'

    # 日志文件存放路径
    log_dir = '/scrapy_gtn/log/'

def get_token():
    return GlobalVar.ts_token
def get_data_dir():
    return GlobalVar.data_dir
def get_log_dir():
    return GlobalVar.log_dir
def get_log_format():
    return GlobalVar.log_format
def get_log_datefmt():
    return GlobalVar.log_datefmt

