CREATE TABLE `stock_basic` (
  `ts_code` varchar(255) DEFAULT NULL COMMENT 'TS代码',
  `symbol` varchar(255) DEFAULT NULL COMMENT '股票代码',
  `name` varchar(255) DEFAULT NULL COMMENT '	股票名称',
  `area` varchar(255) DEFAULT NULL COMMENT '所在地域',
  `industry` varchar(255) DEFAULT NULL COMMENT '所属行业',
  `fullname` varchar(255) DEFAULT NULL COMMENT '股票全称',
  `enname` varchar(255) DEFAULT NULL COMMENT '英文全称',
  `market` varchar(255) DEFAULT NULL COMMENT '市场类型 （主板/中小板/创业板）',
  `exchange` varchar(255) DEFAULT NULL COMMENT '交易所代码',
  `curr_type` varchar(255) DEFAULT NULL COMMENT '交易货币',
  `list_status` varchar(255) DEFAULT NULL COMMENT '上市状态： L上市 D退市 P暂停上市',
  `list_date` varchar(255) DEFAULT NULL COMMENT '上市日期',
  `delist_date` varchar(255) DEFAULT NULL COMMENT '退市日期',
  `is_hs` varchar(255) DEFAULT NULL COMMENT '是否沪深港通标的，N否 H沪股通 S深股通'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='股票列表';
