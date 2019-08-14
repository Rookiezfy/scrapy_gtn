CREATE TABLE `us_stock_list` (
  `symbol` varchar(100) DEFAULT NULL COMMENT '股票代码',
  `market` varchar(50) DEFAULT NULL COMMENT '市场代码-us',
  `stock_name` varchar(255) DEFAULT NULL COMMENT '股票名称',
  UNIQUE KEY `symbol` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='美股股票列表';
