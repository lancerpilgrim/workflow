/* 用户账户信息表 */
CREATE TABLE IF NOT EXISTS `bd_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(64) NOT NULL COMMENT '关联的bd_account.user字段',
  `mask` int(10) unsigned NOT NULL COMMENT '账号标识',
  `value` varchar(128) NOT NULL COMMENT '存储与mask相关的信息字段',
  `note` varchar(256) NOT NULL COMMENT '若微信账号注册，则此字段为appid+tid, 否则为null',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_value` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=2000000 DEFAULT CHARSET=utf8;


/* 壁咚wifi 用户账号*/
CREATE TABLE IF NOT EXISTS `bd_account` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '上网账号',
  `password` varchar(64) NOT NULL COMMENT '上网密码',
  `mask` int(11) unsigned NOT NULL COMMENT '账号标识,mask & (1 << 30) > 0账号被停用',
  `expired` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '用户上网到期时间',
  `ends` int(11) unsigned DEFAULT 1 COMMENT '同时上网终端上限',
  `coin` int(11) unsigned DEFAULT 0 COMMENT '壁咚币, 1壁咚币=10分钟',
  `mobile` varchar(17) NOT NULL DEFAULT '' COMMENT '用户手机号码，组管理员创建账号填写或用户自行绑定',
  `pn` int(11) unsigned DEFAULT NULL COMMENT '账号所属组，只有项目管理员创建的账号带有pn字段',
  `uplink` int(11) unsigned DEFAULT 0 COMMENT '账号上行带宽, 默认为0',
  `downlink` int(11) unsigned DEFAULT 0 COMMENT '账号下行带宽',
  `holder` int(11) DEFAULT NULL COMMENT '房东号',
  `note` varchar(16) DEFAULT '' COMMENT '备注信息，由管理员添加',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_account_user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=200000 DEFAULT CHARSET=utf8;

/* 上网账号和用户设备绑定记录 */
CREATE TABLE IF NOT EXISTS `bd_mac_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '关联的bd_account.user字段',
  `mac` char(17) NOT NULL DEFAULT '' COMMENT '用户设备mac地址',
  `tlogin` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上网终端绑定时间',
  `platform` varchar(256) NOT NULL DEFAULT '' COMMENT '上网设备，User-Agent判断',
  `expired` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '自动认证过期时间',
  `ssid` varchar(32) NOT NULL DEFAULT '' COMMENT 'AP ssid',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mac_history_user_mac` (`user`, `mac`),
  KEY `idx_mac_history_mac` (`mac`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

/*在线设备表*/
CREATE TABLE IF NOT EXISTS `bd_online` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL DEFAULT '' COMMENT '用户上网账号, 关联bd_account.user',
  `nas_addr` varchar(32) NOT NULL DEFAULT '' COMMENT 'AC或认证网关ip地址',
  `acct_session_id` varchar(64) NOT NULL DEFAULT '' COMMENT '会话id, radius查找在线设备依据',
  `acct_start_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上网起始时间',
  `framed_ipaddr` varchar(32) NOT NULL DEFAULT '' COMMENT '终端获得的ip地址',
  `mac_addr` varchar(24) NOT NULL DEFAULT '' COMMENT '终端的mac地址',
  `billing_times` int(11) NOT NULL DEFAULT '0' COMMENT '计费时长',
  `input_total` int(11) NOT NULL DEFAULT '0' COMMENT '下行数据量',
  `output_total` int(11) NOT NULL DEFAULT '0' COMMENT '上行数据量',
  `start_source` smallint(6) NOT NULL DEFAULT '0' COMMENT '状态',
  `ssid` varchar(32) NOT NULL DEFAULT '' COMMENT '联网AP ssid',
  `_location` varchar(64) NOT NULL DEFAULT '' COMMENT '在线设备所在项目',
  `ap_mac` varchar(24) NOT NULL DEFAULT '' COMMENT 'ap mac地址',
  `is_auto` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否通过无感知上线，1: 是，0: 否',
  PRIMARY KEY (`id`),
  KEY `idx_online_user` (`user`),
  UNIQUE KEY `uk_online_mac_addr` (`mac_addr`),
  UNIQUE KEY `uk_online_nas_session_id` (`nas_addr`, `acct_session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

/* AC&网关参数表 */
CREATE TABLE IF NOT EXISTS `bd_bas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor` varchar(32) NOT NULL COMMENT '设备厂商',
  `ip` varchar(15) NOT NULL COMMENT 'ac的工作ip地址（内网或者外网)',
  `name` varchar(64) DEFAULT NULL COMMENT '设备名称',
  `model` varchar(32) DEFAULT NULL COMMENT '设备型号',
  `secret` varchar(64) DEFAULT NULL COMMENT '设备安全字段，Radius报文使用',
  `coa_port` smallint(6) NOT NULL default 3799 COMMENT '管理后台不对改字段做配置',
  `pip` varchar(15) NOT NULL DEFAULT '' COMMENT '映射公网地址',
  `port` smallint(6) unsigned NOT NULL DEFAULT '0' COMMENT '映射公网端口',
  `user` varchar(32) NOT NULL DEFAULT '' COMMENT '用户名',
  `password` varchar(32) NOT NULL DEFAULT '' COMMENT '用户密码 ',
  `mask` int(11) NOT NULL DEFAULT '0' COMMENT 'AC属性bitmap',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;

/* 网关配置，可以理解成特殊的AC */
CREATE TABLE IF NOT EXISTS `bd_gateway` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(32) NOT NULL COMMENT '绑定网关设备ip地址',
  `_location` varchar(32) DEFAULT '' COMMENT '绑定项目location',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_gateway_ip_location` (`ip`, `_location`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* AP 表*/
CREATE TABLE IF NOT EXISTS `bd_ap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(32) NOT NULL COMMENT 'AP mac地址',
  `project_id` varchar(128) DEFAULT '' COMMENT 'AP 所属项目',
  `vendor` varchar(16) DEFAULT NULL COMMENT '品牌',
  `name` varchar(128) DEFAULT NULL COMMENT 'AP名',
  `ip` varchar(16) DEFAULT NULL COMMENT 'AP ip地址',
  `address` varchar(64) DEFAULT NULL COMMENT 'AP地址',
  `ac_ip` varchar(16) DEFAULT NULL COMMENT 'AC ip地址',
  `is_online` tinyint unsigned DEFAULT '0' COMMENT '是否在线，0 - 否，1 - 是',
  `mpoi_id` int(11) DEFAULT NULL COMMENT '地址位置信息字段',
  `connections` int(11) DEFAULT '0' COMMENT '在线人数',
  `model` varchar(32) DEFAULT NULL COMMENT 'ap型号',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `is_sens` tinyint unsigned NOT NULL DEFAULT '0' COMMENT '0-关闭感知/1-开启感知',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ap_mac` (`mac`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* 微信公众号表 */
CREATE TABLE IF NOT EXISTS `bd_wx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '公众号名称',
  `appid` varchar(32) NOT NULL COMMENT '微信公众号appid',
  `secret` varchar(64) NOT NULL COMMENT '公众号secret',
  `token` varchar(64) NOT NULL COMMENT '公众号token',
  `aes_key` varchar(64) NOT NULL COMMENT 'aes加密密钥',
  `note` varchar(128) NOT NULL DEFAULT '' COMMENT '备注',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_wx_appid` (`appid`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

/* 网络配置表 */
CREATE TABLE IF NOT EXISTS `bd_pn_policy` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pn` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '网络项目编号',
  `portal` varchar(64) NOT NULL DEFAULT '' COMMENT '认证页面URI',
  `policy` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '网络配置字段, 使用bit标记信息',
  `note` varchar(128) NOT NULL DEFAULT '' COMMENT '备注',
  `ssid` varchar(24) NOT NULL DEFAULT '' COMMENT '无线ssid',
  `appid` varchar(32) NOT NULL DEFAULT '' COMMENT '微信 app id 用于微信认证上网',
  `shopid` varchar(32) NOT NULL DEFAULT '' COMMENT '门店id, 用于微信认证上网',
  `secret` char(32) NOT NULL DEFAULT '' COMMENT '微信门店安全字段, 信用于微信认证上网',
  `_location` varchar(128) DEFAULT NULL COMMENT '网络所属项目',
  `logo` varchar(128) NOT NULL DEFAULT '/images/bidong.ico',
  `duration` int(11) NOT NULL DEFAULT '30' COMMENT '自动认证间隔时间，默认为30天',
  `session_timeout` int(11) unsigned NOT NULL DEFAULT '24' COMMENT '一次认证，授权时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_pn_policy_pn_ssid` (`pn`,`ssid`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

/* 用户上线下线记录表 */
CREATE TABLE IF NOT EXISTS `bd_ticket` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(64) not null comment '上网账号',
  `acct_session_id` varchar(64) not null comment 'session id',
  `acct_session_time` int not null default 0 comment '上网时长',
  `session_timeout` int not null default 0 comment '',
  `acct_terminate_cause` int not null default 0 comment '连接结束原因,空闲|主动断开|上网到期',
  `acct_input_octets` int default 0 comment '下行数据',
  `acct_output_octets` int default 0 comment '上行数据',
  `acct_input_packets` int default 0 comment '下行数据包',
  `acct_output_packets` int default 0 comment '上行数据包',
  `nas_addr` varchar(24) not null comment 'ac IP地址',
  `mac_addr` varchar(24) not null comment '用户mac地址',
  `ap_mac` varchar(24) not null default '' comment 'ap mac地址',
  `framed_ipaddr` varchar(24) not null default '' comment '用户ip地址',
  `start_source` smallint(6) not null default 0 comment '',
  `stop_source` smallint(6) not null default 0 comment '',
  `acct_start_time` datetime not null default current_timestamp comment '会话起始时间',
  `acct_stop_time` datetime not null default current_timestamp comment '会话结束时间',
  `_location` varchar(128) not null default '' comment '网络所属项目',
   PRIMARY KEY (`id`),
   KEY `idx_ticket_user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

/*  后台项目表 */
CREATE TABLE IF NOT EXISTS `bd_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `_location` varchar(128) NOT NULL COMMENT '项目编号',
  `name` varchar(32) NOT NULL COMMENT '项目名称',
  `license` varchar(128) NOT NULL COMMENT '营业执照图片url',
  `project_type_id` int(11) NOT NULL  COMMENT 'project_type id',
  `mobile` varchar(32) NOT NULL COMMENT '责任人电话',
  `note` text COMMENT '简要说明',
  `address` varchar(32) DEFAULT NULL COMMENT '楼房／店铺地址',
  `owner` varchar(32) NOT NULL COMMENT '责任人',
  `logo` varchar(128) DEFAULT NULL COMMENT 'logo图片url',
  `fieldphoto` varchar(128) DEFAULT NULL COMMENT '实地照片url',
  `tracepoint` varchar(128) DEFAULT NULL COMMENT '地理位置描点图url',
  `topology` varchar(128) DEFAULT NULL COMMENT '拓扑图url',
  `mask` int(11) DEFAULT '1' COMMENT '0-禁用项目/1-启用项目',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '项目开通时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_project_name` (`name`),
  UNIQUE KEY `uk_project_location` (`_location`)
) ENGINE=InnoDB AUTO_INCREMENT=489212 DEFAULT CHARSET=utf8;

/* 项目类型表*/
CREATE TABLE IF NOT EXISTS `bd_project_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(32) DEFAULT NULL COMMENT '类型名称',
  UNIQUE KEY `uk_project_type_label` (`label`),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/* 后台管理员账号 */
CREATE TABLE IF NOT EXISTS `bd_manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) DEFAULT NULL COMMENT '用户名',
  `password` varchar(128) DEFAULT NULL COMMENT '密码',
  `_location` text COMMENT '项目编号',
  `mask` int(11) DEFAULT '1' COMMENT '0-禁用/1-启用',
  `alg` varchar(32) DEFAULT 'md5' COMMENT '密码保存方式',
  `is_root` tinyint unsigned DEFAULT 0 COMMENT '是否为root用户, 1为root用户',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;

/* 权限角色表 */
CREATE TABLE IF NOT EXISTS `bd_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL COMMENT '权限角色名称',
  `_location` varchar(128) NOT NULL DEFAULT '' COMMENT '所属项目',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_location_name` (`name`, `_location`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/* 权限资源表, 把每一个链接作为一个资源控制 */
CREATE TABLE IF NOT EXISTS `bd_permission_resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `banner` varchar(64) NOT NULL COMMENT '资源名称',
  `_resource` varchar(32) NOT NULL COMMENT '资源标识',
  `label` varchar(64) NOT NULL COMMENT '操作名称',
  `action` varchar(32) NOT NULL COMMENT '操作标识',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_permission_resource_action` (`_resource`, `action`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/* 角色的权限控制表 */
CREATE TABLE IF NOT EXISTS `bd_role_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL COMMENT '角色id',
  `resource_id` int(11) NOT NULL COMMENT '资源id',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_role_permission_role` FOREIGN KEY (`role_id`) REFERENCES `bd_role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_role_permission_resource` FOREIGN KEY (`resource_id`) REFERENCES `bd_permission_resource` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 基于角色的权限控制表 */
CREATE TABLE IF NOT EXISTS `bd_acl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '后台管理员登录账号',
  `role_id` int(11) NOT NULL COMMENT '角色id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_acl_user_role` (`user`, `role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 对基于角色权限控制的补充，对具体用户在权限上的增减 */
CREATE TABLE IF NOT EXISTS `bd_addition_acl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '后台管理员登录账号',
  `resource_id` int(11) NOT NULL COMMENT '资源id',
  `mask` tinyint unsigned NOT NULL COMMENT 'mask: 标识位, 0-除去, 1-增加',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_addition_acl_permission_resource` FOREIGN KEY (`resource_id`) REFERENCES `bd_permission_resource` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 上网类型表 */
CREATE TABLE IF NOT EXISTS `bd_web_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL COMMENT '名称',
  `_location` varchar(128) DEFAULT NULL COMMENT '项目编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=391 DEFAULT CHARSET=utf8;

/* 上网套餐表 */
CREATE TABLE IF NOT EXISTS `bd_pay_policy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` decimal(8,2) DEFAULT NULL COMMENT '套餐价格',
  `time` float DEFAULT NULL COMMENT '上网时间（小时）',
  `ends` int(11) DEFAULT NULL COMMENT '同时上网终端数',
  `expired` datetime DEFAULT NULL COMMENT '过期时间',
  `web_type_id` int(11) DEFAULT NULL COMMENT '上网类型id',
  `_location` varchar(128) DEFAULT NULL COMMENT '项目编号',
  `label` varchar(32) DEFAULT '' COMMENT '套餐名称',
  `mask` int(11) DEFAULT NULL COMMENT 'mask & 1 == 1 按小时收费;mask & 1 = 0 按天收费',
  PRIMARY KEY (`id`),
  KEY `idx_pay_policy_web_type_id` (`web_type_id`),
  CONSTRAINT `fk_pay_policy_web_type_id` FOREIGN KEY (`web_type_id`) REFERENCES `bd_web_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=212 DEFAULT CHARSET=utf8;

/* 收款账户设置表 */
CREATE TABLE IF NOT EXISTS `bd_receivable_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `_location` varchar(128) NOT NULL COMMENT '项目编号',
  `platform` varchar(12) NOT NULL COMMENT '支付平台，微信(wechat)或支付宝(alipay)',
  `mch_id` varchar(32) DEFAULT NULL COMMENT '微信mch_id',
  `_key` varchar(64) NOT NULL COMMENT '微信支付key, 或支付宝安全校验码',
  `appid` varchar(32) DEFAULT NULL COMMENT '微信支付appid',
  `seller_id` varchar(32) DEFAULT NULL COMMENT '支付宝商户id',
  `rsa_private_key_url` varchar(64) DEFAULT NULL COMMENT '支付宝证书链接',
  `partner_id` varchar(32) DEFAULT NULL COMMENT '支付宝合作者id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_receivable_account_location_platform` (`_location`, `platform`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 套餐购买记录 */
CREATE TABLE IF NOT EXISTS `bd_pay_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobile` varchar(32) DEFAULT NULL COMMENT '用户手机',
  `fee` decimal(8,2) DEFAULT NULL COMMENT '订单金额',
  `ctime` datetime DEFAULT NULL COMMENT '订单生成时间',
  `mask` int(11) DEFAULT NULL COMMENT 'mask & (1<<7) > 0，苹果内购套餐',
  `platform` varchar(8) DEFAULT NULL COMMENT '支付平台',
  `note` varchar(32) DEFAULT NULL COMMENT '备注',
  `trade_no` varchar(64) DEFAULT NULL COMMENT '订单号',
  `status` varchar(16) DEFAULT NULL COMMENT '订单状态',
  `_location` varchar(128) DEFAULT NULL COMMENT '项目编号',
  `pay_policy_id` int(11) DEFAULT NULL COMMENT '上网套餐id',
  `web_type_id` int(11) DEFAULT NULL COMMENT '上网类型id',
  `user` varchar(128) DEFAULT NULL COMMENT '上网账号',
  `count` int(11) DEFAULT '1' COMMENT '购买份数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66797 DEFAULT CHARSET=utf8;

/* 新闻公告 */
CREATE TABLE IF NOT EXISTS `bd_message` (
  `id` char(32) NOT NULL,
  `title` varchar(128) NOT NULL COMMENT '标题',
  `subtitle` varchar(128) NOT NULL COMMENT '副标题',
  `section` int(11) unsigned NOT NULL DEFAULT '0',
  `mask` tinyint unsigned NOT NULL DEFAULT 0 COMMENT '公告状态, 0 - 发布, 1 - 草稿, 2 - 删除',
  `author` varchar(24) NOT NULL DEFAULT '' COMMENT '创建作者',
  `groups` varchar(64) NOT NULL DEFAULT '' COMMENT '项目组',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `content` text NOT NULL COMMENT '内容',
  `image` varchar(64) NOT NULL DEFAULT '' COMMENT '配图链接',
  `gmtype` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '',
  `labels` varchar(64) NOT NULL DEFAULT '' COMMENT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 兑换码表 */
CREATE TABLE IF NOT EXISTS `bd_redeem_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL COMMENT '兑换码',
  `status` smallint(6) NOT NULL COMMENT '兑换码状态',
  `serial_id` int(11) NOT NULL COMMENT '序列号id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_redeem_code_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8;

/* 兑换码兑换表 */
CREATE TABLE IF NOT EXISTS `bd_redeem_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL COMMENT '兑换码',
  `user` varchar(128) NOT NULL COMMENT '兑换用户id',
  `hours` int(11) NOT NULL COMMENT '兑换时长',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '兑换时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_redeem_record_user_code` (`user`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 兑换码序列号，同一批兑换码可能有上百个 */
CREATE TABLE IF NOT EXISTS `bd_redeem_serial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(128) NOT NULL COMMENT '生成兑换码用户',
  `serial` int(11) NOT NULL COMMENT '兑换码序列号',
  `hours` int(11) NOT NULL COMMENT '兑换码时长',
  `expired` datetime NOT NULL COMMENT '兑换码过期时间',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_redeem_serial_serial` (`serial`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/* 微信号管理表 */
CREATE TABLE IF NOT EXISTS `bd_wechat_promotion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wechat_id` varchar(128) NOT NULL COMMENT '微信号id',
  `nickname` varchar(64) NOT NULL COMMENT '微信号名称',
  `account` varchar(64) NOT NULL COMMENT '微信号登录账号',
  `password` varchar(64) NOT NULL COMMENT '微信登录密码',
  `status` tinyint unsigned NOT NULL DEFAULT 0 COMMENT '推广状态',
  `image_uri` varchar(64) NOT NULL COMMENT '图片链接',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  `is_delete` tinyint unsigned NOT NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
