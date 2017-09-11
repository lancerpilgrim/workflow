/* 用户账户信息表 */
CREATE TABLE IF NOT EXISTS `bd_wechat_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL COMMENT '关联平台用户id',
  `appid` varchar(64) NOT NULL COMMENT '公众号appid',
  `openid` varchar(64) NOT NULL COMMENT '用户openid',
  `mask` int(11) unsigned NOT NULL COMMENT '账号标识, mask & 1 > 0已关注公众号',
  `note` varchar(256) NOT NULL DEFAULT '' COMMENT '备注',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_wechat_user` (`account_id`, `appid`, `openid`)
) ENGINE=InnoDB AUTO_INCREMENT=12000 DEFAULT CHARSET=utf8mb4 COMMENT '账户信息表';


/* 壁咚wifi 平台用户表*/
CREATE TABLE IF NOT EXISTS `bd_account` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '上网账号',
  `password` varchar(128) NOT NULL COMMENT '上网密码',
  `name` varchar(64) COMMENT '用户姓名',
  `nickname` varchar(64) COMMENT '微信昵称',
  `mask` int(11) unsigned NOT NULL DEFAULT 0 COMMENT '账号标识,mask & (1 << 30) > 0账号被停用, mask & 1 > 0 已激活',
  `coin` int(11) unsigned DEFAULT 0 COMMENT '壁咚币, 1壁咚币=10分钟',
  `ends` smallint unsigned DEFAULT 1 COMMENT '同时上网终端上限',
  `mobile` varchar(17) NOT NULL DEFAULT '' COMMENT '用户手机号码',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_account_user` (`user`),
  UNIQUE KEY `uk_account_mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=12000 DEFAULT CHARSET=utf8mb4 COMMENT '用户基础信息表';

/* 项目用户上网策略表, 对公开收费网络，充值或兑换后才能上网，此时生产或更新记录 */
CREATE TABLE IF NOT EXISTS `bd_account_policy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `account_id` int(11) unsigned NOT NULL COMMENT '项目账号关联的平台用户',
  `mask` int(11) NOT NULL DEFAULT 0 COMMENT '项目账号标识,mask & (1 << 30) > 0账号被停用',
  `expired` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '用户上网到期时间, NULL为无限期',
  `ends` int(11) unsigned DEFAULT 1 COMMENT '同时上网终端上限',
  `uplink` int(11) unsigned DEFAULT 0 COMMENT '账号上行带宽, 默认为0',
  `downlink` int(11) unsigned DEFAULT 0 COMMENT '账号下行带宽',
  `pn` varchar(32) NOT NULL COMMENT '所属项目id',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_account_user_pn` (`account_id`, `pn`)
) ENGINE=InnoDB AUTO_INCREMENT=12000 DEFAULT CHARSET=utf8;

/* 项目用户资料表 */
CREATE TABLE IF NOT EXISTS `bd_account_profile` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL COMMENT '归属项目id',
  `account_id` int(11) NOT NULL COMMENT '关联的账号id',
  `name` varchar(64) COMMENT '项目内用户姓名',
  `mobile` varchar(17) COMMENT '用户手机',
  `dyncol` mediumblob COMMENT '动态列',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_profile_pn_mobile` (`pn`, `account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12000 DEFAULT CHARSET=utf8mb4;

/* 系统预设用户表动态属性表 */
CREATE TABLE IF NOT EXISTS `bd_dyncol` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `col` varchar(32) NOT NULL COMMENT '字段名',
  `label` varchar(32) NOT NULL COMMENT '属性名',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dyncol_col_label` (`col`, `label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 项目用户表动态字段表*/
CREATE TABLE IF NOT EXISTS `bd_pn_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL COMMENT '项目编号',
  `dyncol_id` int(11) NOT NULL COMMENT '动态列id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_pnfield_col` (`pn`, `dyncol_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 系统标签库 */
CREATE TABLE IF NOT EXISTS `bd_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_type` varchar(64) NOT NULL COMMENT '标签类型，account, ap etc',
  `name` varchar(32) NOT NULL COMMENT '标签名',
  `pn` int(11) NOT NULL DEFAULT 0 COMMENT '所属项目,默认0为平台标签',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  KEY `idx_pn_tagtype` (`pn`, `tag_type`),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 套餐表 */
CREATE TABLE IF NOT EXISTS `bd_package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT '' COMMENT '套餐名称',
  `price` decimal(8,2) DEFAULT NULL COMMENT '套餐价格',
  `time` float DEFAULT NULL COMMENT '可用上网时长（小时）',
  `ends` smallint DEFAULT NULL COMMENT '同时上网终端数',
  `expired` datetime DEFAULT NULL COMMENT '上网过期时间',
  `available_until` datetime DEFAULT NULL COMMENT '套餐过期时间',
  `pn` int(11) NOT NULL DEFAULT 0 COMMENT '套餐所属项目，0为平台套餐',
  `mask` int(11) NOT  NULL DEFAULT 0 COMMENT '标志位, 第0位: 0 - time 为天, 1 - time 为小时',
  `is_deleted` smallint NOT NULL DEFAULT 0 COMMENT '是否删除, 0 - 否, 1 - 是',
  `apply_projects` varchar(256) NOT NULL DEFAULT '[]' COMMENT '投放项目id列表，空为全部项目',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_package_pn` (`name`, `pn`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 站内信管理表 */
CREATE TABLE IF NOT EXISTS `bd_letter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '通知内容',
  `status` smallint unsigned NOT NULL COMMENT '状态标示, 0 - 草稿, 1 - 发布, 2 - 删除',
  `created_by` int(11) NOT NULL COMMENT '创建平台管理员id',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*  项目管理员站内信表 */
CREATE TABLE IF NOT EXISTS `bd_mailbox` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receiver_id` int(11) COMMENT '管理员id',
  `letter_id` int(11) COMMENT '站内信id',
  `title` varchar(256) COMMENT '标题',
  `content` text COMMENT '通知内容',
  `is_broadcast` smallint unsigned NOT NULL DEFAULT 1 COMMENT '是否广播信息, 0 - 不是, 1 - 是',
  `status` smallint unsigned NOT NULL COMMENT '状态标示, 0 - 未读, 1 - 已读, 2 - 删除',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 上网账号和用户设备绑定 */
CREATE TABLE IF NOT EXISTS `bd_mac_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL COMMENT '关联的bd_account.user字段',
  `mac` char(17) NOT NULL DEFAULT '' COMMENT '用户设备mac地址',
  `tlogin` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上网终端绑定时间',
  `platform` varchar(256) NOT NULL DEFAULT '' COMMENT '上网设备，User-Agent判断',
  `expired` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '自动认证过期时间',
  `ssid` varchar(32) NOT NULL DEFAULT '' COMMENT 'AC ssid',
  PRIMARY KEY (`id`),
  KEY `idx_mac_history_mac` (`mac`),
  UNIQUE KEY `uk_user_mac_ssid` (`user`, `mac`, `ssid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*在线设备表*/
CREATE TABLE IF NOT EXISTS `bd_online` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `pn` int(11) NOT NULL DEFAULT 0 COMMENT '在线设备所在项目, 0为平台',
  `ap_mac` varchar(24) NOT NULL DEFAULT '' COMMENT 'ap mac地址',
  `is_auto` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否通过无感知上线，1: 是，0: 否',
  `auth_type` smallint NOT NULL DEFAULT '0' COMMENT '认证方式，默认为账号密码, 1 -手机号, 2 - 微信, 4 - APP',
  PRIMARY KEY (`id`),
  KEY `idx_online_user` (`user`),
  UNIQUE KEY `uk_online_mac_addr` (`mac_addr`),
  UNIQUE KEY `uk_online_nas_session_id` (`nas_addr`, `acct_session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* AC参数表 */
CREATE TABLE IF NOT EXISTS `bd_ac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '设备名称',
  `vendor` varchar(32) NOT NULL COMMENT '设备厂商',
  `ip` varchar(32) NOT NULL COMMENT 'ac的工作ip地址（内网或者外网)',
  `secret` varchar(64) NOT NULL COMMENT '设备安全字段，Radius报文使用',
  `coa_port` smallint(6) NOT NULL DEFAULT 3799 COMMENT '管理后台不对改字段做配置',
  `pip` varchar(15) NOT NULL DEFAULT '' COMMENT '映射公网地址',
  `port` smallint(6) unsigned NOT NULL DEFAULT '0' COMMENT '映射公网端口',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  UNIQUE KEY `uk_ac_ip` (`ip`),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 微信公众号表 */
CREATE TABLE IF NOT EXISTS `bd_wechat_official_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL COMMENT '所属项目',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '公众号名称',
  `appid` varchar(32) NOT NULL COMMENT '微信公众号appid',
  `shopid` varchar(32) NOT NULL COMMENT '门店ID，用于微信上网',
  `secret` varchar(64) NOT NULL COMMENT '公众号secret',
  `note` varchar(128) NOT NULL DEFAULT '' COMMENT '备注',
  `is_deleted` smallint NOT NULL DEFAULT 0 COMMENT '是否删除',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_wx_appid` (`pn`, `appid`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* portal页配置表 */
CREATE TABLE IF NOT EXISTS `bd_portal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL DEFAULT 0 COMMENT 'portal页面所属项目, 0为平台默认portal页',
  `name` varchar(32) NOT NULL COMMENT 'portal页名称',
  `note` varchar(128) COMMENT '备注',
  `mobile_title` varchar(64) NOT NULL COMMENT '移动端头部文案内容',
  `mobile_banner_url` varchar(256) NOT NULL COMMENT '移动端顶部banner图片链接',
  `pc_title` varchar(64) NOT NULL COMMENT 'PC 文案内容',
  `pc_banner_url` varchar(256) NOT NULL COMMENT 'PC 顶部banner图片链接',
  `on_using` smallint NOT NULL default 0 COMMENT '是否为默认模版, 仅对平台portal模版有意义',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_portal_pn_name` (`pn`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 收款记录 */
CREATE TABLE IF NOT EXISTS `bd_package_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `package_id` int(11) NOT NULL COMMENT '套餐id',
  `account_id` int(11) NOT NULL COMMENT '用户账号id',
  `amount` decimal(8, 2) NOT NULL COMMENT '金额',
  `pay_with` varchar(32) NOT NULL COMMENT '支付方式, alipay or wechat',
  `pay_from` varchar(32) NOT NULL COMMENT '支付入口, APP or wechat',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_pack_order_account_id` FOREIGN KEY (`account_id`) REFERENCES `bd_account` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_pack_order_package_id` FOREIGN KEY (`package_id`) REFERENCES `bd_package` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* API token表 */
CREATE TABLE IF NOT EXISTS `bd_api_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `secret_key` varchar(64) NOT NULL COMMENT 'secret_key',
  `access_token` varchar(128) NOT NULL COMMENT 'access_token',
  `note` varchar(128) NOT NULL COMMENT '备注',
  `mask` int(11) unsigned NOT NULL default 0 COMMENT 'token标志位, mask & 1 > 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_portal_pn_name` (`secret_key`, `access_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* AP 表*/
CREATE TABLE IF NOT EXISTS `bd_ap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(32) NOT NULL COMMENT 'AP mac地址',
  `pn` int(11)  NOT NULL DEFAULT 0 COMMENT 'AP归属的项目ID',
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
  `pn` varchar(128) not null default '' comment '网络所属项目',
   PRIMARY KEY (`id`),
   KEY `idx_ticket_user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;

/* 兑换码表 */
CREATE TABLE IF NOT EXISTS `bd_coupon_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL COMMENT '兑换码',
  `hours` smallint(6) NOT NULL COMMENT '兑换码时长',
  `expired` datetime NOT NULL COMMENT '兑换码过期时间',
  `is_used` smallint(6) NOT NULL DEFAULT 0 COMMENT '是否已被使用',
  `serial_id` int(11) NOT NULL COMMENT '序列号id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_redeem_code_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 兑换码兑换表 */
CREATE TABLE IF NOT EXISTS `bd_coupon_used_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL COMMENT '兑换码',
  `account_id` int(11) NOT NULL COMMENT '兑换用户id',
  `hours` smallint(6) NOT NULL COMMENT '兑换时长',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '兑换时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_redeem_record_user_code` (`account_id`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 同一批兑换码可能有上百个 */
CREATE TABLE IF NOT EXISTS `bd_coupon_serial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_by` int(11) NOT NULL COMMENT '生成兑换码管理员ID',
  `serial` int(11) NOT NULL COMMENT '兑换码序列号',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 网络配置表 */
CREATE TABLE IF NOT EXISTS `bd_network_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pn` int(11) NOT NULL DEFAULT '0' COMMENT '网络项目编号',
  `ssid` varchar(32) NOT NULL DEFAULT '' COMMENT '无线ssid',
  `portal_id` int(11) NOT NULL DEFAULT 0 COMMENT '认证portal配置ID, 0为默认模版',
  `is_public` smallint NOT NULL DEFAULT 1 COMMENT '是否为私有网络, 0为公有',
  `is_free` smallint NOT NULL DEFAULT 1 COMMENT '计费方式, 0 - 收费, 1 - 免费',
  `mask` int(11) NOT NULL COMMENT '认证方式, 前三位表示, 0 - 手机号, 1 - 微信, 2 - APP, 如 mask=7则全部支持',
  `wechat_account_id` int(11) COMMENT '微信认证上网公众账号, 仅当 mask & 2 > 0时使用',
  `duration` int(11) NOT NULL DEFAULT 30 COMMENT '自动认证间隔时间，默认为30天',
  `session_timeout` int(11)  NOT NULL DEFAULT 24 COMMENT '一次认证，授权时间（小时)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '兑换时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pn_network_config_pn_ssid` (`pn`,`ssid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 用户标签 */
CREATE TABLE IF NOT EXISTS `bd_account_tag` (
  `account_id` int(11) NOT NULL COMMENT '账号id',
  `tag_id` int(11) NOT NULL COMMENT '标签id',
  PRIMARY KEY (`account_id`, `tag_id`),
  CONSTRAINT `fk_actag_account_id` FOREIGN KEY (`account_id`) REFERENCES `bd_account` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_actag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `bd_tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 套餐对应的用户标签 */
CREATE TABLE IF NOT EXISTS `bd_package_tag` (
  `package_id` int(11) NOT NULL COMMENT '套餐id',
  `tag_id` int(11) NOT NULL COMMENT '标签id',
  PRIMARY KEY (`package_id`, `tag_id`),
  CONSTRAINT `fk_packtag_package_id` FOREIGN KEY (`package_id`) REFERENCES `bd_package` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_packtag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `bd_tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* AP标签表 */
CREATE TABLE IF NOT EXISTS `bd_ap_tag` (
  `ap_id` int(11) NOT NULL COMMENT 'AP id',
  `tag_id` int(11) NOT NULL COMMENT '标签id',
  PRIMARY KEY (`ap_id`, `tag_id`),
  CONSTRAINT `fk_aptag_ap_id` FOREIGN KEY (`ap_id`) REFERENCES `bd_ap` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_aptag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `bd_tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT 'name of the project',
  `description` varchar(256) NOT NULL DEFAULT '' COMMENT 'brief of the project',
  `location` varchar(256) NOT NULL DEFAULT '' COMMENT 'As its literal meaning',
  `contact` varchar(64) NOT NULL DEFAULT '' COMMENT 'As its literal meaning',
  `contact_number` bigint(20) NOT NULL DEFAULT '0' COMMENT '联系电话',
  `email` varchar(128) NOT NULL DEFAULT '' COMMENT 'contact''s e-mail',
  `status` tinyint(5) NOT NULL DEFAULT '1' COMMENT '状态，2为删除，1为可用，0为不可用',
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP COMMENT '当前时间戳',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `projects_authorization`;
CREATE TABLE `projects_authorization` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `authorization_holder` bigint(20) NOT NULL DEFAULT '0' COMMENT '被授权主体的身份ID, 默认为项目的project_id',
  `resource_name` varchar(64) NOT NULL DEFAULT '' COMMENT '资源名称, public_name',
  `resource_locator` varchar(128) NOT NULL DEFAULT '' COMMENT '资源定位符, 一个具体资源在其所属类别中的标识符，根据resource_id和resource_locator可以定位到一个资源, 类似uri的作用，留空时表示该类别中的所有资源',
  `holder_type` smallint(5) NOT NULL DEFAULT '0' COMMENT '被授权主体的类型,可以是项目组, 默认为0,代表单个项目,将来扩展时详细定义',
  `resource_id` int(11) NOT NULL COMMENT '资源id, 对应于resource_registry表中的id字段',
  `allow_method` smallint(5) NOT NULL DEFAULT '15' COMMENT '参考Linux文件权限, 8为读，4为增，2为改, 1为删，如有多个权限，累加。判断是否有某个权限时，比如最终结果为15，15&8 = 8 那么则为有读权限。',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否生效，1为是，0为否',
  `resource_amount` int(11) NOT NULL DEFAULT '1' COMMENT '如果该授权的资源具有数量限制，则为授权数量，默认为1',
  `effective_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '授权生效时间，时间戳',
  `expiration_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '授权过期时间，时间戳',
  PRIMARY KEY (`id`),
  UNIQUE KEY `authorization_holder` (`authorization_holder`,`resource_name`,`resource_locator`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `resources_registry`;
CREATE TABLE `resources_registry` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '资源的注册id，做成自增',
  `resource_type` smallint(5) NOT NULL DEFAULT '0' COMMENT '资源类型，暂时未定义，留待将来使用',
  `public_name` varchar(128) NOT NULL DEFAULT '' COMMENT '资源公有名称，要求全局唯一',
  `private_name` varchar(128) NOT NULL DEFAULT '' COMMENT '资源私有名称，用来拼接uri',
  `description` varchar(256) NOT NULL DEFAULT '0' COMMENT '资源的描述',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否有效，1为是，0为否',
  PRIMARY KEY (`id`),
  UNIQUE KEY `KET` (`public_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `resources_tree`;
CREATE TABLE `resources_tree` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ancestor` int(10) NOT NULL DEFAULT '0' COMMENT '祖先资源id',
  `descendant` int(10) NOT NULL DEFAULT '0' COMMENT '后代资源id',
  `ancestor_name` varchar(64) NOT NULL DEFAULT '' COMMENT '祖先资源名称, private_name, 如果我们的API采用统一的url生成方案, 可以直接根据规则拼接出来',
  `descendant_name` varchar(64) NOT NULL DEFAULT '' COMMENT '后代资源名称, private_name',
  `distance` int(11) NOT NULL COMMENT '祖先到后代在树上的距离',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ancestor_descendant` (`ancestor`,`descendant`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
