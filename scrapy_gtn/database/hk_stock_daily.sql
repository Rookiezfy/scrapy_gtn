CREATE TABLE `hk_stock_daily` (
  `ts_code` varchar(255) NOT NULL COMMENT '股票代码',
  `trade_date` varchar(255) NOT NULL COMMENT '交易日期',
  `open` decimal(40,2) DEFAULT NULL COMMENT '开盘价',
  `high` decimal(40,2) DEFAULT NULL COMMENT '最高价',
  `low` decimal(40,2) DEFAULT NULL COMMENT '最低价',
  `close` decimal(40,2) DEFAULT NULL COMMENT '收盘价',
  `vol` decimal(40,2) DEFAULT NULL COMMENT '成交量',
  `amount` decimal(40,2) DEFAULT NULL COMMENT '成交额(元)',
  `query_code` varchar(255) DEFAULT NULL COMMENT '用于东财接口查询的代码，市场代码.股票代码',
   primary key(ts_code,trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='港股日线行情';
