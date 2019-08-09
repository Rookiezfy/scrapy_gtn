CREATE TABLE `hk_hs_stock_list` (
  `secid` varchar(100) DEFAULT NULL COMMENT '唯一id,用于东财查询行情',
  `market` varchar(50) DEFAULT NULL COMMENT '市场代码 116-港股 1-上证A 0-深证A',
  `stock_code` varchar(50) DEFAULT NULL COMMENT '股票代码',
  `stock_name` varchar(100) DEFAULT NULL COMMENT '股票名称',
  UNIQUE KEY `secid` (`secid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='港股 沪深A股 股票列表';