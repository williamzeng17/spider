# coding: utf-8

from commonDB import CommonDB
import database

#db sql
'''
CREATE TABLE `paper` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增索引',
  `title` varchar(256) NOT NULL DEFAULT '' COMMENT '标题',
  `url` varchar(256) NOT NULL DEFAULT '' COMMENT '文章地址',
  `author` varchar(11) NOT NULL DEFAULT '' COMMENT '作者',
  `abstract` varchar(512) NOT NULL DEFAULT '' COMMENT '文章摘要',
  `read_cnt` int(11) NOT NULL DEFAULT '0' COMMENT '阅读数',
  `comment_cnt` int(11) NOT NULL DEFAULT '0' COMMENT '评论数',
  `like_cnt` int(11) NOT NULL DEFAULT '0' COMMENT '点赞数',
  `reward_cnt` int(11) NOT NULL DEFAULT '0' COMMENT '打赏数',
  `_status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '数据状态',
  `_create_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '创建时间',
  `_modify_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `pub_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '发表时间',
  `content` text NOT NULL COMMENT '内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
'''

class PaperDao(CommonDB):
    def __init__(self):
        """

        """
        CommonDB.__init__(self, database.config['spider'])
        self.table = 'paper'
        self.primaryKey = 'id'
        self.keys = [
            'id',
            'title',
            'url',
            'author',
            'abstract',
            'content',
            'read_cnt',
            'comment_cnt',
            'like_cnt',
            'reward_cnt',
            '_status',
            '_create_time',
            '_modify_time'
        ]
