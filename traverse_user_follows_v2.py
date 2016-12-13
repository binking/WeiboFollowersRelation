#coding=utf-8
import sys
import time
import redis
import argparse
import traceback
from datetime import datetime as dt
import multiprocessing as mp
from decrators import catch_database_error
from utils import create_processes
from config import MAIL_CURL_DICT, REDIS_KEY
from weibo_kol_spider_v3 import get_user_follow_list, get_follow_pages
from database_operator import read_user_url_from_db, insert_follow_into_db

reload(sys)
sys.setdefaultencoding('utf-8')


def follow_info_generator(url_jobs, follow_results):
    """
    Producer for urls and topics, Consummer for topics
    """
    cp = mp.current_process()
    while True:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Generate Follows Process pid is %d" % (cp.pid)
        user_url, page_num = url_jobs.get()
        follow_list = get_user_follow_list(user_url, page_num)
        # if follow_list:  # except access_time and url
        if not follow_list:
            print "Tried over and over again, can not get follows"
        for follow in follow_list:
            follow_results.put(follow)
        url_jobs.task_done()


def follow_db_writer(follow_results):
    """
    Consummer for topics
    """
    cp = mp.current_process()
    while True:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Write Follow Process pid is %d" % (cp.pid)
        info_dict = follow_results.get()
        # print info_dict
        write_status = insert_follow_into_db(info_dict)
        follow_results.task_done()


def add_url_jobs(target):
    todo = 0
    list_of_kw = read_user_url_from_db()
    if not list_of_kw:
        return -1
    for kw in list_of_kw:
        todo += 1
        try:
            pages = get_follow_pages(kw)
            if not pages:  # pages must >= 1, 0 means failed
                continue
            for page in range(1, pages+1):
                target.put((kw, page))
        except Exception as e:
            print e
        # if todo > 1:
        #     break
    return todo


def run_all_worker():
    try:
        # load weibo account into redis cache
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        for mail in MAIL_CURL_DICT:
            r.sadd(REDIS_KEY, mail)

        # Producer is on !!!
        url_jobs = mp.JoinableQueue()
        follow_results = mp.JoinableQueue()
        create_processes(follow_info_generator, (url_jobs, follow_results), 4)
        create_processes(follow_db_writer, (follow_results, ), 8)

        cp = mp.current_process()
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Run All Works Process pid is %d" % (cp.pid)
        num_of_users = add_url_jobs(url_jobs)
        print "<"*10,
        print "There are %d users to process" % num_of_users, 
        print ">"*10
        url_jobs.join()
        follow_results.join()
        print "+"*10, "url_jobs' length is ", url_jobs.qsize()
        print "+"*10, "follow_results' length is ", follow_results.qsize()
    except Exception as e:
        traceback.print_exc()
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Exception raise in runn all Work"
    except KeyboardInterrupt:
        print dt.now().strftime("%Y-%m-%d %H:%M:%S"), "Interrupted by you and quit in force, but save the results"
        print "+"*10, "url_jobs' length is ", url_jobs.qsize()
        print "+"*10, "follow_results' length is ", follow_results.qsize()


def single_process():
    # load weibo account into redis cache
    todo=0
    list_of_kw = read_user_url_from_db()
    if not list_of_kw:
        return -1
    for kw in list_of_kw:
        todo += 1
        max_page = get_follow_pages(kw)
        print max_page
        follow_list = get_user_follow_list(kw, 1)
        for follow in follow_list:
            insert_follow_into_db(follow)
        if todo > 1:
            break

if __name__=="__main__":
    print "\n" + "%s Began Update Weibo Follows" % dt.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    start = time.time()
    run_all_worker()
    # single_process()
    print "*"*10, "Totally Update Weibo Follows Time Consumed : %d seconds" % (time.time() - start), "*"*10
