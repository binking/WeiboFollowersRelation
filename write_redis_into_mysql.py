#coding=utf-8
import os
import sys
import time
import redis
import random
import pickle
import argparse
import traceback
from datetime import datetime as dt
import multiprocessing as mp
from requests.exceptions import ConnectionError
from zc_spider.weibo_config import (
    FOLLOWS_JOBS_CACHE, FOLLOWS_RESULTS_CACHE,
    WEIBO_ERROR_TIME, WEIBO_ACCESS_TIME,
    WEIBO_ACCOUNT_PASSWD, WEIBO_CURRENT_ACCOUNT,
    TOPIC_URL_CACHE, TOPIC_INFO_CACHE,
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


def user_db_writer(cache):
    """
    Consummer for topics
    """
    error_count = 0
    cp = mp.current_process()
    dao = WeiboFollowWriter(USED_DATABASE)
    while True:
        # if error_count > 999:
        #     print '>'*10, 'Exceed 1000 times of write errors', '<'*10
        #     break
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Write Follow Process pid is %d" % (cp.pid)
        temp = cache.blpop(FOLLOWS_RESULTS_CACHE, 0)[1]
        try:
            res = pickle.loads(temp)
            if not isinstance(res, dict) and len(str(res)) > 10000:
                print str(res).replace('\\', '')
                continue
            dao.insert_follow_into_db(res)   # ////// broken up, cuz res is string
        except Exception as e:  # won't let you died
            pickle_len = len(str(res))
            print 'Failed to write result: %d, there was %d times of errors' % (pickle_len, error_count)
            error_count += 1
            if pickle_len < 10000 and pickle_len != 440:
                cache.rpush(FOLLOWS_RESULTS_CACHE, temp)
            time.sleep(2)
        except KeyboardInterrupt as e:
            print "Interrupted in Write process"
            cache.rpush(FOLLOWS_RESULTS_CACHE, temp)
            break


def run_multiple_writer():
    result_cache = redis.StrictRedis(**USED_REDIS)  # list
    # import ipdb; ipdb.set_trace()
    # create_processes(user_db_writer, (result_cache, ), 8)
    threads = []
    try:
        # for _ in range(8):
        #     threads.append(threading.Thread(target=user_db_writer, args=(result_cache, )))
        # for i in range(8):
        #     threads[i].start()
        # for i in range(8):
        #     threads[i].join()
        p = mp.Pool(processes=4, initializer=user_db_writer, initargs=(result_cache, ))
        p.close()
        p.join()
    except Exception as e:
        print "Exception Occured: " + str(e)
    except KeyboardInterrupt as e:
        print "Interrupted by You: " + str(e)
    print "All done"

if __name__=="__main__":
    print "\n\n" + "%s Began Scraped Weibo User Follows" % dt.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    start = time.time()
    run_multiple_writer()
    # single_process()
    print "*"*10, "Totally Scraped Weibo User Follows Time Consumed : %d seconds" % (time.time() - start), "*"*10
