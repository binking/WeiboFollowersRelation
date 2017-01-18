#-*- coding: utf-8 -*-
#--------  话题48992  爬取一个话题下的所有微博  --------
import os
import sys
import time
import redis
from datetime import datetime as dt
from zc_spider.weibo_config import (
    FOLLOWS_JOBS_CACHE,  # weibo:blog:urls
    QCLOUD_MYSQL, OUTER_MYSQL,
    LOCAL_REDIS, QCLOUD_REDIS
)
from weibo_follow_writer import WeiboFollowWriter

reload(sys)
sys.setdefaultencoding('utf-8')

if os.environ.get('SPIDER_ENV') == 'test':
    print "*"*10, "Run in Test environment"
    USED_DATABASE = OUTER_MYSQL
    USED_REDIS = LOCAL_REDIS
elif 'centos' in os.environ.get('HOSTNAME'): 
    print "*"*10, "Run in Qcloud environment"
    USED_DATABASE = QCLOUD_MYSQL
    USED_REDIS = QCLOUD_REDIS
else:
    raise Exception("Unknown Environment, Check it now...")


def add_jobs(target):
    todo = 0
    dao = WeiboFollowWriter(USED_DATABASE)
    for job in dao.read_user_url_from_db():  # iterate
        todo += 1
        urls = []
        for ind in range(5):  # suppose 5 pages
            urls.append('%s/follow?page=%d' % (job, ind+1))
        for url in urls:
            if target.lrem(FOLLOWS_JOBS_CACHE, 0, url):
                target.lpush(FOLLOWS_JOBS_CACHE, url)
            else:
                target.rpush(FOLLOWS_JOBS_CACHE, url)
            # target.rpush(FOLLOWS_JOBS_CACHE, job)
    print 'There are totally %d jobs to process' % todo
    return todo

if __name__=='__main__':
    print "\n\n" + "%s Began Scraped Weibo User Follows" % dt.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    start = time.time()
    r = redis.StrictRedis(**USED_REDIS)
    add_jobs(r)
    print "*"*10, "Totally Time Consumed : %d seconds" % (time.time() - start), "*"*10
    
