#coding=utf-8
import os
import sys
import time
import redis
import pickle
from datetime import datetime as dt
import  multiprocessing
import threading
from requests.exceptions import ConnectionError
from template.weibo_config import (
    WEIBO_MANUAL_COOKIES, MANUAL_COOKIES,
    WEIBO_ACCOUNT_PASSWD,
    JOBS_QUEUE, RESULTS_QUEUE,
    DEPRECATE_FOLLOW, INSERT_FOLLOW_SQL,
    QCLOUD_MYSQL, OUTER_MYSQL,
    LOCAL_REDIS, QCLOUD_REDIS
)
from template.weibo_utils import create_processes
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
        if error_count > 999:
            print '>'*10, 'Exceed 1000 times of write errors', '<'*10
            break
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Write Follow Process pid is %d" % (cp.pid)
        res = cache.blpop(FOLLOWS_RESULTS_CACHE, 0)[1]
        try:
            res = pickle.loads(res)
            if not isinstance(res, dict) and len(str(res)) > 10000:
                print str(res).replace('\\', '')
                continue
            dao.insert_follow_into_db(res)   # ////// broken up, cuz res is string
        except Exception as e:  # won't let you died
            print 'Failed to write result: ', len(pickle.loads(res))
            error_count += 1
            if len(str(pickle.loads(res))) < 10000:
                cache.rpush(FOLLOWS_RESULTS_CACHE, pickle.dumps(res))
        except KeyboardInterrupt as e:
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
        p = multiprocessing.Pool(processes=8, initializer=user_db_writer, initargs=(result_cache, ))
        p.close()
        p.join()
    except Exception as e:
        print str(e)
    except KeyboardInterrupt as e:
        print str(e)
    print "All done"

if __name__=="__main__":
    print "\n\n" + "%s Began Scraped Weibo User Follows" % dt.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    start = time.time()
    run_multiple_writer()
    # single_process()
    print "*"*10, "Totally Scraped Weibo User Follows Time Consumed : %d seconds" % (time.time() - start), "*"*10
