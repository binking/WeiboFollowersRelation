#coding=utf-8
import sys
import time
import traceback
from datetime import datetime as dt
import MySQLdb as mdb
from zc_spider.weibo_writer import DBAccesor, database_error_hunter
reload(sys)
sys.setdefaultencoding('utf-8')


class WeiboFollowWriter(DBAccesor):

    def __init__(self, db_dict):
        DBAccesor.__init__(self, db_dict)

    def connect_database(self):
        return DBAccesor.connect_database(self)

    # @database_error_hunter
    def insert_follow_into_db(self, res):
        insert_sql = """
            INSERT INTO weibouserfollows
            (nickname, weibo_user_url, follow_nickname, follow_fans_num, follow_weibo_num, 
            follow_focus_num, follow_type, follow_usercard, createdate, is_up2date)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Y'
            FROM DUAL WHERE NOT EXISTS (SELECT id FROM weibouserfollows 
            WHERE weibo_user_url = %s and follow_usercard = %s and is_up2date = 'Y')
        """
        conn = self.connect_database()
        cursor = conn.cursor()
        try:
            if cursor.execute(insert_sql, (
                res['myname'], res['url'], 
                res.get('name', ''), res.get('fans', ''), 
                res.get('blogs', ''), res.get('follows', ''),
                res.get('type', ''), res['usercard'], 
                res['date'], res['url'], res['usercard']
            )):
                print '$'*10, 'Write follow info succeeded !'
                conn.commit(); 
            cursor.close(); conn.close()
        except Exception as e:
            traceback.print_exc()
            conn.commit(); cursor.close(); conn.close()
            raise Exception(str(e))

    # @database_error_hunter
    def read_user_url_from_db(self):
        select_user_sql = """
            SELECT DISTINCT wu.weibo_user_url
            FROM topicinfo t, topicweiborelation tw, weibocomment wc, weibouser wu  
            WHERE t.topic_url = tw.topic_url 
            AND tw.weibo_url = wc.weibo_url 
            AND wc.weibocomment_author_url = wu.weibo_user_url 
            AND wu.createdate > DATE_SUB(DATE(now()), INTERVAL '1' DAY)
        """
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute(select_user_sql)
        for res in cursor.fetchall():
            yield res[0]

    @database_error_hunter
    def read_repost_user_from_db(self):
        select_sql = """
            SELECT DISTINCT CONCAT('http://weibo.com/', wr.weibo_user_id)
            FROM weiboreposts wr
            WHERE not EXISTS (
            SELECT * from weibouserfollows wuf
            WHERE wuf.weibo_user_url=CONCAT('http://weibo.com/', wr.weibo_user_id)
            );
        """
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute(select_sql)
        for res in cursor.fetchall():
            yield res[0]
        '''
        select_user_sql = """
            SELECT DISTINCT wu.weibo_user_url 
            FROM topicinfo t, topicweiborelation tw, weibocomment wc, weibouser wu
            # WHERE t.id in (21520,1016,23952,8180,21362,7031)
            WHERE t.topic_url = tw.topic_url
            AND tw.weibo_url = wc.weibo_url
            AND wc.weibocomment_author_url = wu.weibo_user_url
            AND wu.createdate > '2016-12-13'
            -- AND wu.id % 3 = 0
        """
        select_existed_user = """
            SELECT DISTINCT weibo_user_url
            FROM weibouserfollows
            WHERE is_up2date='Y'
        """
        conn = self.connect_database()
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        cursor1.execute(select_user_sql)
        cursor2.execute(select_existed_user)
        done_list = []
        todo_list = []
        for res in cursor2.fetchall():
            done_list.append(res[0])
        for res in cursor1.fetchall():
            if res[0] not in done_list:
                # yield res[0]
                todo_list.append(res[0])
        return todo_list
        '''
