#coding=utf-8
import os
import sys
import time
import redis
import argparse
import traceback
from datetime import datetime as dt
import multiprocessing as mp
from requests.exceptions import ConnectionError
from template.weibo_config import (
    WEIBO_MANUAL_COOKIES, MANUAL_COOKIES,
    WEIBO_ACCOUNT_PASSWD, 
    JOBS_QUEUE, RESULTS_QUEUE,
    DEPRECATE_FOLLOW, INSERT_FOLLOW_SQL,
    QCLOUD_MYSQL, OUTER_MYSQL,
    LOCAL_REDIS, QCLOUD_REDIS
)
from template.weibo_utils import (
    create_processes,
    pick_rand_ele_from_list
)
from weibo_follow_spider import WeiboFollowSpider
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


def add_jobs(cache):
    todo = 0
    dao = WeiboFollowWriter(USED_DATABASE)
    jobs = dao.read_user_url_from_db()
    for job in jobs:  # iterate
        todo += 1
        print "Adding %d-th job into redis....." % todo
        try:
            all_account = cache.hkeys(MANUAL_COOKIES)
            if not all_account:  # no any weibo account
                raise Exception('All of your accounts were Freezed')
            account = pick_rand_ele_from_list(all_account)
            spider = WeiboFollowSpider(job+'/follow?page=1', account, WEIBO_ACCOUNT_PASSWD, timeout=20)
            spider.add_request_header()
            spider.use_cookie_from_curl(WEIBO_MANUAL_COOKIES[account])
            # spider.use_cookie_from_curl(TEST_CURL_SER)
            spider.gen_html_source()
            for ind in range(spider.get_max_page_no()):
                cache.rpush(JOBS_QUEUE, '%s/follow?page=%d' % (job, ind+1))
        except Exception as e:
            print e
    return todo

if __name__=='__main__':
    job_cache = redis.StrictRedis(**USED_REDIS)  # list
    # result_cache = redis.StrictRedis(**USED_REDIS)  # list
    if not job_cache.llen(JOBS_QUEUE):  # divide init and other machines
        add_jobs(job_cache)