#coding=utf8
from fabric.api import *
from zc_spider.weibo_config import SERVER_LIST, SERVER_LOGIN_INFO

env.hosts = SERVER_LIST

env.passwords = SERVER_LOGIN_INFO

def update():
    with cd('/PythonProject/WeiboFollowersRelation'):
        run('git pull')

def execute():
    with cd('/PythonProject/WeiboFollowersRelation'):
        run('/home/jiangzhibin/PythonProgramming/ZhicangSpiders/spider_env/bin/python scraping_weibo_followers_v2.py >> ~/spider_log/weibo_follow.log 2>&1 &')

