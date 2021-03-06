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
    WEIBO_NORMAL_COOKIES, MANUAL_COOKIES,
    WEIBO_ACCOUNT_PASSWD, 
    JOBS_QUEUE, RESULTS_QUEUE,
    DEPRECATE_FOLLOW, INSERT_FOLLOW_SQL,
    QCLOUD_MYSQL, OUTER_MYSQL,
    LOCAL_REDIS, QCLOUD_REDIS
)
from zc_spider.weibo_utils import create_processes
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

TEST_CURL_SER = "curl 'http://weibo.com/p/1005051791434577/follow?page=5' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=dfbc5c548bac6a6a5e37d19076c4c674; ALF=1484881079; SUB=_2A251XZ_nDeTxGeNH41YS9C7EyzyIHXVWoSGvrDV8PUJbkNAKLWTCkW2NPaiM8gFhxA0bsw3KWB6ZhjO72A..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5jjvRuP4Nkie-qT9gjG1GY5NHD95Qf1KnXe0B71h57Ws4Dqcj_i--4iKLFi-zci--NiKnpi-8Fi--ciKLhi-8Wi--ciKL2iKn0i--fi-iFi-iW; TC-Page-G0=b05711a62e11e2c666cc954f2ef362fb; _s_tentry=-; Apache=9691795277147.832.1482289229381; SINAGLOBAL=9691795277147.832.1482289229381; ULV=1482289229395:1:1:1:9691795277147.832.1482289229381:; TC-V5-G0=6fd5dedc9d0f894fec342d051b79679e' -H 'Connection: keep-alive' --compressed"

def user_info_generator(cache1, cache2):
    """
    Producer for users(cache1) and follows(cache2), Consummer for topics
    """
    cp = mp.current_process()
    while True:
        res = {}
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Generate Follow Process pid is %d" % (cp.pid)
        job = cache1.blpop(JOBS_QUEUE, 0)[1]   # blpop 获取队列数据
        try:
            all_account = cache1.hkeys(MANUAL_COOKIES)
            if not all_account:  # no any weibo account
                raise Exception('All of your accounts were Freezed')
            # account = pick_rand_ele_from_list(all_account)
            account = "qianldbf6835@163.com"
            # operate spider
            spider = WeiboFollowSpider(job, account, WEIBO_ACCOUNT_PASSWD, timeout=20)
            spider.use_abuyun_proxy()
            spider.add_request_header()
            spider.use_cookie_from_curl(WEIBO_NORMAL_COOKIES[account])
            # spider.use_cookie_from_curl(TEST_CURL_SER)
            spider.gen_html_source()
            f_list = spider.get_user_follow_list()
            if f_list:
                for follow in f_list:
                    # d_sql = DEPRECATE_FOLLOW.format(
                    #     user=follow['url'],
                    #     followid=follow['usercard'])
                    i_sql = INSERT_FOLLOW_SQL.format(
                        nickname=follow['myname'], user=follow['url'],
                        follow=follow.get('name', ''), fans=follow.get('fans', ''),
                        blogs=follow.get('blogs', ''), focus=follow.get('follows', ''),
                        type=follow.get('type', ''), followid=follow['usercard'],
                        date=follow['date'], status='Y')
                    # format sql and push them into result queue
                    cache2.rpush(RESULTS_QUEUE, '%s||%s' % (d_sql, i_sql))  # push ele to the tail
        except Exception as e:  # no matter what was raised, cannot let process died
            # cache1.rpush(JOBS_QUEUE, job) # put job back
            print 'Raised in gen process', str(e)
        except KeyboardInterrupt as e:
            break


def user_db_writer(cache):
    """
    Consummer for topics
    """
    cp = mp.current_process()
    dao = WeiboFollowWriter(USED_DATABASE)
    while True:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Write Follow Process pid is %d" % (cp.pid)
        res = cache.blpop(RESULTS_QUEUE, 0)[1]
        try:
            d_sql, i_sql = res.split('||')
            dao.insert_follow_into_db(d_sql, i_sql)
        except Exception as e:  # won't let you died
            print 'Raised in write process', str(e)
            cache.rpush(RESULTS_QUEUE, res)
        except KeyboardInterrupt as e:
            break
            

def add_jobs(cache):
    todo = 0
    print "Adding jobs into redis....."
    dao = WeiboFollowWriter(USED_DATABASE)
    jobs = dao.read_user_url_from_db()
    for job in jobs:  # iterate
        todo += 1
        try:
            all_account = cache.hkeys(MANUAL_COOKIES)
            if not all_account:  # no any weibo account
                raise Exception('All of your accounts were Freezed')
            account = pick_rand_ele_from_list(all_account)
            spider = WeiboFollowSpider(job+'/follow?page=1', account, WEIBO_ACCOUNT_PASSWD, timeout=20)
            spider.add_request_header()
            spider.use_cookie_from_curl(WEIBO_NORMAL_COOKIES[account])
            # spider.use_cookie_from_curl(TEST_CURL_SER)
            spider.gen_html_source()
            for ind in range(spider.get_max_page_no()):
                cache.rpush(JOBS_QUEUE, '%s/follow?page=%d' % (job, ind+1))
        except Exception as e:
            print e
    return todo


def run_all_worker():
    job_cache = redis.StrictRedis(**USED_REDIS)  # list
    result_cache = redis.StrictRedis(**USED_REDIS)  # list
    if not job_cache.llen(JOBS_QUEUE):  # divide init and other machines
        add_jobs(job_cache)
    else:
        print "Redis have %d records in cache" % job_cache.llen(JOBS_QUEUE)
    job_pool = mp.Pool(processes=4,
        initializer=user_info_generator, initargs=(job_cache, result_cache))
    result_pool = mp.Pool(processes=8, 
        initializer=user_db_writer, initargs=(result_cache, ))
    cp = mp.current_process()
    print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Run All Works Process pid is %d" % (cp.pid)
    try:
        job_pool.close()
        result_pool.close()
        job_pool.join()
        result_pool.join()
        print "+"*10, "jobs' length is ", job_cache.llen(JOBS_QUEUE) #jobs.llen(JOBS_QUEUE)
        print "+"*10, "results' length is ", result_cache.llen(RESULTS_QUEUE) #jobs.llen(JOBS_QUEUE)
    except Exception as e:
        traceback.print_exc()
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Exception raise in runn all Work"
    except KeyboardInterrupt:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Interrupted by you and quit in force, but save the results"
        print "+"*10, "jobs' length is ", job_cache.llen(JOBS_QUEUE) #jobs.llen(JOBS_QUEUE)
        print "+"*10, "results' length is ", result_cache.llen(RESULTS_QUEUE) #jobs.llen(JOBS_QUEUE)

def single_process():
    cache = redis.StrictRedis(**USED_REDIS)
    account = "jiedaf7816@163.com"
    for _ in range(5):
        job = cache.blpop(JOBS_QUEUE, 0)[1]
        spider = WeiboFollowSpider(job, account, 'tttt5555', timeout=20)
        spider.use_abuyun_proxy()
        spider.add_request_header()
<<<<<<< HEAD
        # spider.use_cookie_from_curl(cache.hget(MANUAL_COOKIES, account))
        spider.use_cookie_from_curl(TEST_CURL_SER)
=======
        spider.use_cookie_from_curl(WEIBO_NORMAL_COOKIES[account])
        # spider.use_cookie_from_curl(TEST_CURL_SER)
>>>>>>> baba8f8282af3d5509ee0f916173bb11b6e70da4
        spider.gen_html_source()
        f_list = spider.get_user_follow_list()
        for f in f_list:
            print f
        cache.rpush(JOBS_QUEUE, job)

if __name__=="__main__":
    print "\n\n" + "%s Began Scraped Weibo User Follows" % dt.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    start = time.time()
    # run_all_worker()
    single_process()
    print "*"*10, "Totally Scraped Weibo User Follows Time Consumed : %d seconds" % (time.time() - start), "*"*10
