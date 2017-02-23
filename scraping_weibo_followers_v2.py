#coding=utf-8
import os
import sys
import time
import redis
import random
import pickle
import traceback
from datetime import datetime as dt
import multiprocessing as mp
from requests.exceptions import ConnectionError
from zc_spider.weibo_config import (
    WEIBO_COOKIES, FOLLOWS_JOBS_CACHE, FOLLOWS_RESULTS_CACHE,
    WEIBO_ACCOUNT_PASSWD, INACTIVE_USER_CACHE,
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

TEST_CURL_SER = "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=52765f5018c5d34c5f77302463042cdf; ALF=1484204272; SUB=_2A251S-ugDeTxGeNH41cV8CbLyTWIHXVWt_XorDV8PUJbkNAKLWbBkW0_fe7_8gLTd0veLjcMNIpRdG9dKA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhZLMdo2m4y1PHxGYdNTkzk5JpX5oz75NHD95Qf1KnfSh5RS0z4Ws4Dqcj_i--ciKLsi-z0i--RiK.pi-2pi--ci-zfiK.0i--fi-zEi-zRi--ciKy2i-2E; TC-Page-G0=cdcf495cbaea129529aa606e7629fea7' -H 'Connection: keep-alive' --compressed"



def user_info_generator(cache):
    """
    Producer for users(cache) and follows(cache2), Consummer for topics
    """
    error_count = 0
    loop_count = 0
    cp = mp.current_process()
    while True:
        res = {}
        loop_count += 1
        if error_count > 9999:
            print '>'*10, 'Exceed 10000 times of gen errors', '<'*10
            break
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Generate Follow Process pid is %d" % (cp.pid)
        job = cache.blpop(FOLLOWS_JOBS_CACHE, 0)[1]   # blpop 获取队列数据
        try:
            # operate spider
            all_account = cache.hkeys(WEIBO_COOKIES)
            if len(all_account) == 0:
                time.sleep(pow(2, loop_count))
                continue
            account = random.choice(all_account)
            spider = WeiboFollowSpider(job, account, WEIBO_ACCOUNT_PASSWD, timeout=20)
            spider.use_abuyun_proxy()
            spider.add_request_header()
            spider.use_cookie_from_curl(cache.hget(WEIBO_COOKIES, account))
            # spider.use_cookie_from_curl(TEST_CURL_SER)
            status = spider.gen_html_source()
            if status in [404, 20003]:
                continue
            f_list = spider.get_user_follow_list()
            for follow in f_list:
                cache.rpush(FOLLOWS_RESULTS_CACHE, pickle.dumps(follow))  # push string to the tail
        except Exception as e:  # no matter what was raised, cannot let process died
            cache.rpush(FOLLOWS_JOBS_CACHE, job) # put job back
            print 'Parse %s Error: ' % job + str(e)
            error_count += 1
        except KeyboardInterrupt as e:
            print "Interrupted in Spider process"
            cache.rpush(FOLLOWS_JOBS_CACHE, job) # put job back
            break


def run_all_worker():
    job_cache = redis.StrictRedis(**USED_REDIS)  # list
    print "Redis have %d records in cache" % job_cache.llen(FOLLOWS_JOBS_CACHE)
    job_pool = mp.Pool(processes=8,
        initializer=user_info_generator, initargs=(job_cache, ))
    cp = mp.current_process()
    print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Run All Works Process pid is %d" % (cp.pid)
    try:
        job_pool.close()
        job_pool.join()
    except Exception as e:
        traceback.print_exc()
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Exception raise in runn all Work"
    except KeyboardInterrupt:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Interrupted by you and quit in force, but save the results"
    print "+"*10, "jobs' length is ", job_cache.llen(FOLLOWS_JOBS_CACHE) #jobs.llen(FOLLOWS_JOBS_CACHE)
    print "+"*10, "results' length is ", job_cache.llen(FOLLOWS_RESULTS_CACHE) #jobs.llen(FOLLOWS_JOBS_CACHE)


if __name__=="__main__":
    print "\n\n" + "%s Began Scraped Weibo User Follows" % dt.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    start = time.time()
    run_all_worker()
    # single_process()
    print "*"*10, "Totally Scraped Weibo User Follows Time Consumed : %d seconds" % (time.time() - start), "*"*10
