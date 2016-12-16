#coding=utf-8
import os
import sys
import time
import redis
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

TEST_CURL_SER = "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=52765f5018c5d34c5f77302463042cdf; ALF=1484204272; SUB=_2A251S-ugDeTxGeNH41cV8CbLyTWIHXVWt_XorDV8PUJbkNAKLWbBkW0_fe7_8gLTd0veLjcMNIpRdG9dKA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhZLMdo2m4y1PHxGYdNTkzk5JpX5oz75NHD95Qf1KnfSh5RS0z4Ws4Dqcj_i--ciKLsi-z0i--RiK.pi-2pi--ci-zfiK.0i--fi-zEi-zRi--ciKy2i-2E; TC-Page-G0=cdcf495cbaea129529aa606e7629fea7' -H 'Connection: keep-alive' --compressed"


def user_db_writer(results):
    """
    Consummer for topics
    """
    cp = multiprocessing.current_process()
    dao = WeiboFollowWriter(USED_DATABASE)
    while True:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Write Follow Process pid is %d" % (cp.pid)
        res = results.blpop(JOBS_QUEUE, 0)
        # print res
        print "Bingo"
        # res = results.get(results)
        try:
            d_sql, i_sql = res[1].split('||')
            print d_sql
            print i_sql
            dao.insert_follow_into_db(d_sql, i_sql)
            # cache.rpush(res)
        except Exception as e:  # won't let you died
            print 'Raised in write process', str(e)
            results.rpush(res)
        except KeyboardInterrupt as e:
            print (e)
            break
            # results.put(res)

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
    # time.sleep(5)

"""
    dao = WeiboFollowWriter(USED_DATABASE)
    while True:
        res = result_cache.blpop(JOBS_QUEUE)
        print "Ya lu "
        # res = results.get(results)
        try:
            if not res:
                print 'Game is done '
                break
            d_sql, i_sql = res.split('||')
            dao.insert_follow_into_db(d_sql, i_sql)
            # cache.rpush(res)
        except Exception as e:  # won't let you died
            print 'Raised in write process', str(e)
            result_cache.rpush(JOBS_QUEUE, res)
"""

if __name__=='__main__':
    run_multiple_writer()