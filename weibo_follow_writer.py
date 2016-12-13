#coding=utf-8
import sys
import time
import traceback
from datetime import datetime as dt
import MySQLdb as mdb
from template.weibo_writer import DBAccesor, database_error_hunter
reload(sys)
sys.setdefaultencoding('utf-8')


class WeiboFollowWriter(DBAccesor):

    def __init__(self, db_dict):
        DBAccesor.__init__(self, db_dict)

    def connect_database(self):
        return DBAccesor.connect_database(self)

    @database_error_hunter
    def insert_follow_into_db(self, deprecate_sql, insert_sql):
        conn = self.connect_database()
        if not conn:
            return False
        cursor = conn.cursor()
        if cursor.execute(deprecate_sql):
            print '$'*10, 'Deprecate %d follows succeeded !' % cursor.rowcount
        if cursor.execute(insert_sql):
            print '$'*10, 'Write follow info succeeded !'
        conn.commit(); cursor.close(); conn.close()
        return True


    @database_error_hunter
    def read_user_url_from_db(self):
        select_user_sql = """
            SELECT DISTINCT wu.weibo_user_url 
            FROM topicinfo t, topicweiborelation tw, weibocomment wc, weibouser wu
            # WHERE t.id in (21520,1016,23952,8180,21362,7031)
            WHERE t.topic_url = tw.topic_url
            AND tw.weibo_url = wc.weibo_url
            AND wc.weibocomment_author_url = wu.weibo_user_url
            AND wu.createdate > '2016-12-01'
        """
        conn = self.connect_database()
        cursor1 = conn.cursor()
        cursor1.execute(select_user_sql)
        for res in cursor1.fetchall():
            # if res[0] not in done_list:
            yield res[0]
    