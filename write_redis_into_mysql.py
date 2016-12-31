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