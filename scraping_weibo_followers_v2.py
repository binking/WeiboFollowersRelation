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

TEST_CURL_SER = "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=52765f5018c5d34c5f77302463042cdf; ALF=1484204272; SUB=_2A251S-ugDeTxGeNH41cV8CbLyTWIHXVWt_XorDV8PUJbkNAKLWbBkW0_fe7_8gLTd0veLjcMNIpRdG9dKA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhZLMdo2m4y1PHxGYdNTkzk5JpX5oz75NHD95Qf1KnfSh5RS0z4Ws4Dqcj_i--ciKLsi-z0i--RiK.pi-2pi--ci-zfiK.0i--fi-zEi-zRi--ciKy2i-2E; TC-Page-G0=cdcf495cbaea129529aa606e7629fea7' -H 'Connection: keep-alive' --compressed"

def user_info_generator(cache):
    """
    Producer for users(cache) and follows(cache2), Consummer for topics
    """
    cp = mp.current_process()
    while True:
        res = {}
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Generate Follow Process pid is %d" % (cp.pid)
        job = cache.blpop(JOBS_QUEUE, 0)[1]   # blpop 获取队列数据
        try:
            all_account = cache.hkeys(MANUAL_COOKIES)
            if not all_account:  # no any weibo account
                raise Exception('All of your accounts were Freezed')
            account = pick_rand_ele_from_list(all_account)
            # operate spider
            spider = WeiboFollowSpider(job, account, WEIBO_ACCOUNT_PASSWD, timeout=20)
            spider.use_abuyun_proxy()
            spider.add_request_header()
            # spider.use_cookie_from_curl(WEIBO_MANUAL_COOKIES[account])
            spider.use_cookie_from_curl(cache.hget(MANUAL_COOKIES, account))
            # spider.use_cookie_from_curl(TEST_CURL_SER)
            spider.gen_html_source()
            f_list = spider.get_user_follow_list()
            if f_list:
                for follow in f_list:
                    d_sql = DEPRECATE_FOLLOW.format(
                        user=follow['url'],
                        followid=follow['usercard'])
                    i_sql = INSERT_FOLLOW_SQL.format(
                        nickname=follow['myname'], user=follow['url'],
                        follow=follow.get('name', ''), fans=follow.get('fans', ''),
                        blogs=follow.get('blogs', ''), focus=follow.get('follows', ''),
                        type=follow.get('type', ''), followid=follow['usercard'],
                        date=follow['date'], status='Y')
                    # format sql and push them into result queue
                    cache.rpush(RESULTS_QUEUE, '%s||%s' % (d_sql, i_sql))  # push ele to the tail
        except Exception as e:  # no matter what was raised, cannot let process died
            cache.rpush(JOBS_QUEUE, job) # put job back
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
            print 'Raised in write process\n', str(e)
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
            spider.use_cookie_from_curl(WEIBO_MANUAL_COOKIES[account])
            # spider.use_cookie_from_curl(TEST_CURL_SER)
            spider.gen_html_source()
            for ind in range(spider.get_max_page_no()):
                cache.rpush(JOBS_QUEUE, '%s/follow?page=%d' % (job, ind+1))
        except Exception as e:
            print e
    return todo


def run_all_worker():
    job_cache = redis.StrictRedis(**USED_REDIS)  # list
    # result_cache = redis.StrictRedis(**USED_REDIS)  # list
    if not job_cache.llen(JOBS_QUEUE):  # divide init and other machines
        add_jobs(job_cache)
    else:
        print "Redis have %d records in cache" % job_cache.llen(JOBS_QUEUE)
    job_pool = mp.Pool(processes=4,
        initializer=user_info_generator, initargs=(job_cache, ))
    result_pool = mp.Pool(processes=8, 
        initializer=user_db_writer, initargs=(job_cache, ))
    cp = mp.current_process()
    print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Run All Works Process pid is %d" % (cp.pid)
    try:
        job_pool.close()
        result_pool.close()
        job_pool.join()
        result_pool.join()
        print "+"*10, "jobs' length is ", job_cache.llen(JOBS_QUEUE) #jobs.llen(JOBS_QUEUE)
        print "+"*10, "results' length is ", job_cache.llen(RESULTS_QUEUE) #jobs.llen(JOBS_QUEUE)
    except Exception as e:
        traceback.print_exc()
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Exception raise in runn all Work"
    except KeyboardInterrupt:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Interrupted by you and quit in force, but save the results"
        print "+"*10, "jobs' length is ", job_cache.llen(JOBS_QUEUE) #jobs.llen(JOBS_QUEUE)
        print "+"*10, "results' length is ", job_cache.llen(RESULTS_QUEUE) #jobs.llen(JOBS_QUEUE)


if __name__=="__main__":
    print "\n\n" + "%s Began Scraped Weibo User Follows" % dt.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    start = time.time()
    run_all_worker()
    # single_process()
    print "*"*10, "Totally Scraped Weibo User Follows Time Consumed : %d seconds" % (time.time() - start), "*"*10
