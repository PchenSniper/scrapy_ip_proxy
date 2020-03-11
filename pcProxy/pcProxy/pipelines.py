# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class MysqlPipeline(object):
    # 将数据保存于MySQL的Item Pipeline
    def open_spider(self, spider):
        # Spider开启时，获取数据库配置信息，连接MySQL数据库服务
        host = spider.settings.get("MYSQL_HOST", "localhost")
        user = spider.settings.get("MYSQL_USER", "sql")
        pwd = spider.settings.get("MYSQL_PASSWORD", "123456")
        db_name = spider.settings.get("MYSQL_DB_NAME", "ipProxy")
        # 连接MySQL数据库服务
        self.db_conn = MySQLdb.connect(
            db=db_name,
            host=host,
            user=user,
            password=pwd,
            charset="utf8",
        )
        # 获取游标
        self.db_cursor = self.db_conn.cursor()

    def process_item(self, item, spider):
        # 将数据保存于MySQL
        tb_name = spider.settings.get("MYSQL_TB_NAME", "proxy")
        values = (
            item['ip'],
            item['port'],
            item['anonymity_levels'],
            item['protocol'],
            item['position'],
            item['country'],
        )
        sql = 'insert into {tb_name}(ip, port, anonymity_levels'.format(tb_name=tb_name) + \
            ', protocol, position, country) values (%s, %s, %s, %s, %s, %s)'
        self.db_cursor.execute(sql, values)
        return item

    def close_spider(self, spider):
        # Spider关闭，执行数据库关闭工作
        self.db_conn.commit()
        self.db_cursor.close()
        self.db_conn.close()
